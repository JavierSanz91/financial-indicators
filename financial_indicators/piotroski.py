"""
Piotroski F-Score: Financial strength indicator (0-9).

Developed by Stanford accounting professor Joseph Piotroski (2000).
Higher scores indicate stronger financial position.

Reference:
    Piotroski, J.D. (2000). "Value Investing: The Use of Historical Financial
    Statement Information to Separate Winners from Losers."
    Journal of Accounting Research, 38, 1-41.
"""

from typing import Optional


def f_score(
    roa: float,
    roa_prev: float,
    ocf: float,
    total_assets: float,
    leverage: float,
    leverage_prev: float,
    current_ratio: float,
    current_ratio_prev: float,
    shares_outstanding: int,
    shares_outstanding_prev: int,
    gross_margin: float,
    gross_margin_prev: float,
    asset_turnover: float,
    asset_turnover_prev: float,
) -> int:
    """
    Calculate the Piotroski F-Score (0-9).

    The score is based on 9 binary criteria across 3 groups:
    - Profitability (4 points)
    - Leverage/Liquidity (3 points)
    - Operating Efficiency (2 points)

    Args:
        roa: Return on Assets (current year)
        roa_prev: Return on Assets (previous year)
        ocf: Operating Cash Flow (current year)
        total_assets: Total Assets (current year)
        leverage: Long-term debt / Total assets (current year)
        leverage_prev: Long-term debt / Total assets (previous year)
        current_ratio: Current assets / Current liabilities (current year)
        current_ratio_prev: Current assets / Current liabilities (previous year)
        shares_outstanding: Shares outstanding (current year)
        shares_outstanding_prev: Shares outstanding (previous year)
        gross_margin: Gross profit / Revenue (current year)
        gross_margin_prev: Gross profit / Revenue (previous year)
        asset_turnover: Revenue / Total assets (current year)
        asset_turnover_prev: Revenue / Total assets (previous year)

    Returns:
        Integer score from 0 (weakest) to 9 (strongest).
        8-9 = Strong. 0-2 = Weak.
    """
    score = 0

    # --- Profitability (4 criteria) ---
    # 1. Positive ROA
    if roa > 0:
        score += 1

    # 2. Positive Operating Cash Flow
    if ocf > 0:
        score += 1

    # 3. Increasing ROA
    if roa > roa_prev:
        score += 1

    # 4. Cash flow > ROA (accruals check)
    if total_assets > 0 and (ocf / total_assets) > roa:
        score += 1

    # --- Leverage, Liquidity, Source of Funds (3 criteria) ---
    # 5. Decreasing leverage
    if leverage < leverage_prev:
        score += 1

    # 6. Increasing current ratio
    if current_ratio > current_ratio_prev:
        score += 1

    # 7. No new share issuance
    if shares_outstanding <= shares_outstanding_prev:
        score += 1

    # --- Operating Efficiency (2 criteria) ---
    # 8. Increasing gross margin
    if gross_margin > gross_margin_prev:
        score += 1

    # 9. Increasing asset turnover
    if asset_turnover > asset_turnover_prev:
        score += 1

    return score


def interpret(score: int) -> str:
    """
    Interpret a Piotroski F-Score.

    Args:
        score: F-Score value (0-9)

    Returns:
        Human-readable interpretation string.
    """
    if score >= 8:
        return "Strong - Company shows robust financial health across all dimensions"
    elif score >= 6:
        return "Good - Company is financially sound with minor concerns"
    elif score >= 4:
        return "Moderate - Mixed financial signals, requires deeper analysis"
    elif score >= 2:
        return "Weak - Multiple financial red flags present"
    else:
        return "Very Weak - Significant financial distress indicators"


def breakdown(
    roa: float,
    roa_prev: float,
    ocf: float,
    total_assets: float,
    leverage: float,
    leverage_prev: float,
    current_ratio: float,
    current_ratio_prev: float,
    shares_outstanding: int,
    shares_outstanding_prev: int,
    gross_margin: float,
    gross_margin_prev: float,
    asset_turnover: float,
    asset_turnover_prev: float,
) -> dict:
    """
    Get a detailed breakdown of each Piotroski F-Score criterion.

    Returns:
        Dictionary with score, interpretation, and per-criterion details.
    """
    criteria = {
        "positive_roa": {
            "name": "Positive ROA",
            "group": "Profitability",
            "passed": roa > 0,
            "value": roa,
        },
        "positive_ocf": {
            "name": "Positive Operating Cash Flow",
            "group": "Profitability",
            "passed": ocf > 0,
            "value": ocf,
        },
        "increasing_roa": {
            "name": "Increasing ROA",
            "group": "Profitability",
            "passed": roa > roa_prev,
            "value": roa - roa_prev,
        },
        "accruals_check": {
            "name": "Cash Flow > ROA (Accruals)",
            "group": "Profitability",
            "passed": total_assets > 0 and (ocf / total_assets) > roa,
            "value": (ocf / total_assets) - roa if total_assets > 0 else None,
        },
        "decreasing_leverage": {
            "name": "Decreasing Leverage",
            "group": "Leverage & Liquidity",
            "passed": leverage < leverage_prev,
            "value": leverage - leverage_prev,
        },
        "increasing_current_ratio": {
            "name": "Increasing Current Ratio",
            "group": "Leverage & Liquidity",
            "passed": current_ratio > current_ratio_prev,
            "value": current_ratio - current_ratio_prev,
        },
        "no_dilution": {
            "name": "No Share Dilution",
            "group": "Leverage & Liquidity",
            "passed": shares_outstanding <= shares_outstanding_prev,
            "value": shares_outstanding - shares_outstanding_prev,
        },
        "increasing_gross_margin": {
            "name": "Increasing Gross Margin",
            "group": "Operating Efficiency",
            "passed": gross_margin > gross_margin_prev,
            "value": gross_margin - gross_margin_prev,
        },
        "increasing_asset_turnover": {
            "name": "Increasing Asset Turnover",
            "group": "Operating Efficiency",
            "passed": asset_turnover > asset_turnover_prev,
            "value": asset_turnover - asset_turnover_prev,
        },
    }

    total = sum(1 for c in criteria.values() if c["passed"])

    return {
        "score": total,
        "interpretation": interpret(total),
        "criteria": criteria,
    }
