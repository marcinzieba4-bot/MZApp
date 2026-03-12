"""
Poland Pivot Opportunity Framework — AWS Lambda Handler
=======================================================
Returns Polish WSE pivot opportunity ideas as structured JSON.

Supports:
  GET /          — all 6 ideas
  GET /?ticker=LBW      — single idea by ticker
  GET /?idea_type=SOTP  — filter by idea type (partial match)
  GET /?full=true       — include full thesis text
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from examples.poland_asymmetric_ideas import IDEAS


# ─── helpers ──────────────────────────────────────────────────────────────────

def _pw_return(idea):
    bear = (idea["bear_target"] / idea["current_price"] - 1) * 100
    base = (idea["base_target"] / idea["current_price"] - 1) * 100
    bull = (idea["bull_target"] / idea["current_price"] - 1) * 100
    return round(bear * idea["bear_p"] + base * idea["base_p"] + bull * idea["bull_p"], 2)


def _asymmetry(idea):
    up = idea["bull_target"] / idea["current_price"] - 1
    dn = abs(idea["bear_target"] / idea["current_price"] - 1)
    return round(up / dn, 2) if dn else 99.0


def _serialize(idea, full_text=False):
    out = {
        "rank":             idea["rank"],
        "name":             idea["name"],
        "ticker":           idea["ticker"],
        "exchange":         "WSE",
        "sector":           idea["sector"],
        "idea_type":        idea["idea_type"],
        "market_cap_m_pln": idea.get("market_cap_m_pln"),
        "market_cap_m_eur": idea.get("market_cap_m_eur"),
        "entry_price":      idea["current_price"],
        "currency":         idea["currency"],
        "valuation": {
            "pe":                    idea.get("pe"),
            "ev_ebitda":             idea.get("ev_ebitda"),
            "pb":                    idea.get("pb"),
            "roe_pct":               idea.get("roe_pct"),
            "ebitda_margin_pct":     idea.get("ebitda_margin_pct"),
            "revenue_m":             idea.get("revenue_m"),
            "revenue_growth_yoy_pct":idea.get("revenue_growth_yoy_pct"),
            "net_cash_m":            idea.get("net_cash_m"),
        },
        "ownership": {
            "insider_pct":       idea.get("insider_pct"),
            "institutional_pct": idea.get("institutional_pct"),
            "analyst_count":     idea.get("analyst_count"),
        },
        "scenarios": {
            "bear": {"target": idea["bear_target"], "probability": idea["bear_p"], "irr_pct": idea.get("bear_irr")},
            "base": {"target": idea["base_target"], "probability": idea["base_p"], "irr_pct": idea.get("base_irr")},
            "bull": {"target": idea["bull_target"], "probability": idea["bull_p"], "irr_pct": idea.get("bull_irr")},
        },
        "pw_return_pct":   _pw_return(idea),
        "asymmetry_ratio": _asymmetry(idea),
        "catalyst":        idea.get("catalyst"),
        "key_risk":        idea.get("key_risk"),
        "time_horizon":    idea.get("time_horizon"),
        "hf_style":        idea.get("hf_style"),
        "thesis_summary":  (idea.get("why_asymmetric") or "")[:600].strip(),
    }
    if full_text:
        out["thesis_full"] = idea.get("why_asymmetric", "")
    return out


def _resp(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False, default=str),
    }


# ─── handler ──────────────────────────────────────────────────────────────────

def handler(event, context):
    """
    AWS Lambda entry point. Works with both API Gateway (proxy integration)
    and Lambda Function URLs.
    """
    params       = event.get("queryStringParameters") or {}
    ticker_f     = (params.get("ticker") or "").strip().upper()
    type_f       = (params.get("idea_type") or "").strip().upper()
    full_text    = str(params.get("full", "false")).lower() == "true"
    sort_by_pwr  = str(params.get("sort", "rank")).lower() == "pw_return"

    ideas = list(IDEAS)

    if ticker_f:
        ideas = [i for i in ideas if i["ticker"].upper() == ticker_f]
    if type_f:
        ideas = [i for i in ideas if type_f in i["idea_type"].upper()]

    if not ideas:
        return _resp(404, {
            "error": "No ideas found matching criteria",
            "available_tickers": [i["ticker"] for i in IDEAS],
            "filters_applied": params,
        })

    if sort_by_pwr:
        ideas = sorted(ideas, key=_pw_return, reverse=True)

    result = [_serialize(i, full_text=full_text) for i in ideas]

    return _resp(200, {
        "market":       "Warsaw Stock Exchange (WSE)",
        "report_date":  "March 2026",
        "framework":    "Pivot Opportunity Framework",
        "total_ideas":  len(result),
        "ideas":        result,
    })
