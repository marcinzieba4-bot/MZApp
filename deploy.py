#!/usr/bin/env python3
"""
deploy.py — Package and deploy the MSCI Poland Lambda function using boto3.
Usage: python deploy.py
"""

import os, sys, shutil, zipfile, subprocess, time, tempfile

import boto3
from botocore.exceptions import ClientError

# ── Config ────────────────────────────────────────────────────────────────────
# Credentials are read from environment variables — never hardcode them here.
# Set before running:
#   export AWS_ACCESS_KEY_ID=...
#   export AWS_SECRET_ACCESS_KEY=...
AWS_ACCESS_KEY_ID     = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
REGION         = "eu-west-1"
FUNCTION_NAME  = "msci-poland-inclusion-report"
RUNTIME        = "python3.11"
TIMEOUT        = 120
MEMORY         = 512
HANDLER        = "lambda_handler.handler"
SENDER_EMAIL   = "marcin.zieba4@gmail.com"
RECIPIENT_EMAIL = "marcin.zieba@yahoo.com"

# Existing role that already has AWSLambdaBasicExecutionRole + AmazonSESFullAccess
ROLE_ARN = "arn:aws:iam::905418356298:role/service-role/daily-trends-digest-role-9ru0fj04"

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH     = os.path.join(PROJECT_ROOT, "lambda_package.zip")

# ── Helpers ───────────────────────────────────────────────────────────────────
def session():
    return boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION,
    )

def build_zip() -> bytes:
    """Install deps into temp dir, copy source, zip it all up."""
    tmp = tempfile.mkdtemp(prefix="msci_lambda_")
    print(f"  Working dir: {tmp}")

    print("  pip install reportlab boto3 ...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "reportlab", "boto3",
         "-q", "--target", tmp],
        stdout=subprocess.DEVNULL,
    )

    for item in ("examples", "framework", "lambda_handler.py"):
        src = os.path.join(PROJECT_ROOT, item)
        dst = os.path.join(tmp, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tmp):
            # Skip __pycache__ to keep zip smaller
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                full = os.path.join(root, file)
                arc  = os.path.relpath(full, tmp)
                zf.write(full, arc)

    shutil.rmtree(tmp)
    size_mb = os.path.getsize(ZIP_PATH) / 1_000_000
    print(f"  ZIP: {ZIP_PATH}  ({size_mb:.1f} MB)")
    with open(ZIP_PATH, "rb") as f:
        return f.read()

def ensure_ses_verified(ses, email: str):
    """Best-effort: trigger verification. If user lacks ses:Get* just skip."""
    try:
        resp = ses.get_identity_verification_attributes(Identities=[email])
        attrs = resp["VerificationAttributes"].get(email, {})
        status = attrs.get("VerificationStatus", "")
        if status == "Success":
            print(f"  ✓ {email} already verified")
        else:
            ses.verify_email_identity(EmailAddress=email)
            print(f"  ✉  Verification email sent to {email} — check inbox and click the link")
    except ClientError as e:
        if "AccessDenied" in str(e):
            # User doesn't have ses:Get* — the Lambda role has SES permissions,
            # which is what matters at runtime. Skip the check here.
            print(f"  (skipping SES check for {email} — no ses:Get* permission; "
                  f"Lambda role has AmazonSESFullAccess)")
        else:
            raise

def deploy_lambda(lam, zip_bytes: bytes):
    env = {
        "Variables": {
            "SENDER_EMAIL": SENDER_EMAIL,
            "RECIPIENT_EMAIL": RECIPIENT_EMAIL,
            "SES_REGION": REGION,
        }
    }
    try:
        lam.get_function(FunctionName=FUNCTION_NAME)
        exists = True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            exists = False
        else:
            raise

    if exists:
        print(f"  Updating function code ...")
        lam.update_function_code(
            FunctionName=FUNCTION_NAME,
            ZipFile=zip_bytes,
        )
        waiter = lam.get_waiter("function_updated")
        waiter.wait(FunctionName=FUNCTION_NAME)
        lam.update_function_configuration(
            FunctionName=FUNCTION_NAME,
            Timeout=TIMEOUT,
            MemorySize=MEMORY,
            Environment=env,
        )
        waiter.wait(FunctionName=FUNCTION_NAME)
        print(f"  Updated.")
    else:
        print(f"  Creating function ...")
        lam.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime=RUNTIME,
            Role=ROLE_ARN,
            Handler=HANDLER,
            Code={"ZipFile": zip_bytes},
            Timeout=TIMEOUT,
            MemorySize=MEMORY,
            Environment=env,
            Description="Generates MSCI Poland inclusion PDFs and emails them via SES",
        )
        waiter = lam.get_waiter("function_active")
        waiter.wait(FunctionName=FUNCTION_NAME)
        print(f"  Created.")

    fn = lam.get_function(FunctionName=FUNCTION_NAME)
    return fn["Configuration"]["FunctionArn"]

def add_monthly_schedule(events, lam, function_arn: str):
    """EventBridge rule: 1st of month at 08:00 UTC."""
    rule_name = f"{FUNCTION_NAME}-monthly"
    rule = events.put_rule(
        Name=rule_name,
        ScheduleExpression="cron(0 8 1 * ? *)",
        State="ENABLED",
        Description="Monthly MSCI Poland report — 1st of month 08:00 UTC",
    )
    rule_arn = rule["RuleArn"]

    events.put_targets(
        Rule=rule_name,
        Targets=[{"Id": "1", "Arn": function_arn}],
    )

    try:
        lam.add_permission(
            FunctionName=FUNCTION_NAME,
            StatementId="EventBridgeMonthly",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=rule_arn,
        )
    except ClientError as e:
        if "ResourceConflictException" not in str(e):
            raise

    print(f"  Schedule: {rule_arn}")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    s   = session()
    ses = s.client("ses")
    lam = s.client("lambda")
    evb = s.client("events")

    print("\n1. Verifying SES email identities ...")
    ensure_ses_verified(ses, SENDER_EMAIL)
    ensure_ses_verified(ses, RECIPIENT_EMAIL)

    print("\n2. Building Lambda ZIP ...")
    zip_bytes = build_zip()

    print("\n3. Deploying Lambda function ...")
    fn_arn = deploy_lambda(lam, zip_bytes)
    print(f"  ARN: {fn_arn}")

    print("\n4. Setting up monthly EventBridge schedule ...")
    try:
        add_monthly_schedule(evb, lam, fn_arn)
    except ClientError as e:
        if "AccessDenied" in str(e):
            print("  ⚠  No events:PutRule permission — schedule not created.")
            print("     Add it manually in the Lambda console: Triggers → EventBridge")
            print("     Schedule: cron(0 8 1 * ? *)  [1st of month, 08:00 UTC]")
        else:
            raise

    print(f"""
✓  Done!

Function : {FUNCTION_NAME}
Region   : {REGION}
ARN      : {fn_arn}
Schedule : 1st of every month at 08:00 UTC

To invoke now:
  python -c "
import boto3, json
lam = boto3.client('lambda', region_name='{REGION}')
r = lam.invoke(FunctionName='{FUNCTION_NAME}', InvocationType='RequestResponse')
print(json.loads(r['Payload'].read()))
"

⚠  If email addresses show 'check inbox', verify them before the Lambda sends.
""")

if __name__ == "__main__":
    main()
