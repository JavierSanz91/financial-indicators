"""
Beneish M-Score: Earnings manipulation detection model.

Developed by Professor Messod D. Beneish at Indiana University (1999).
Identifies the probability that a company has manipulated its reported earnings.

Reference:
    Beneish, M.D. (1999). "The Detection of Earnings Manipulation."
    Financial Analysts Journal, 55(5), 24-36.
"""


def m_score(
    dsri: float,
    gmi: float,
    aqi: float,
    sgi: float,
    depi: float,
    sgai: float,
    tata: float,
    lvgi: float,
) -> float:
    """
    Calculate the Beneish M-Score.

    Formula:
        M = -4.84 + 0.920*DSRI + 0.528*GMI + 0.404*AQI + 0.892*SGI
            + 0.115*DEPI - 0.172*SGAI + 4.679*TATA - 0.327*LVGI

    Args:
        dsri: Days Sales in Receivables Index
        gmi: Gross Margin Index
        aqi: Asset Quality Index
        sgi: Sales Growth Index
        depi: Depreciation Index
        sgai: SGA Expense Index
        tata: Total Accruals to Total Assets
        lvgi: Leverage Index

    Returns:
        M-Score float value.
        > -1.78: Company is likely a manipulator
        < -1.78: Company is unlikely to be a manipulator
    """
    return (
        -4.84
        + 0.920 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
        - 0.172 * sgai
        + 4.679 * tata
        - 0.327 * lvgi
    )


def calculate_variables(
    net_receivables: float,
    net_receivables_prev: float,
    sales: float,
    sales_prev: float,
    cogs: float,
    cogs_prev: float,
    current_assets: float,
    current_assets_prev: float,
    ppe: float,
    ppe_prev: float,
    securities: float,
    securities_prev: float,
    total_assets: float,
    total_assets_prev: float,
    depreciation: float,
    depreciation_prev: float,
    sga: float,
    sga_prev: float,
    current_liabilities: float,
    current_liabilities_prev: float,
    lt_debt: float,
    lt_debt_prev: float,
    income_continuing: float,
    cash_from_operations: float,
) -> dict:
    """
    Calculate all 8 Beneish M-Score variables from raw financial data.

    Returns:
        Dictionary with all 8 variables and the final M-Score.
    """
    # DSRI: Days Sales in Receivables Index
    dsri = (net_receivables / sales) / (net_receivables_prev / sales_prev) if sales_prev > 0 and net_receivables_prev > 0 else 1.0

    # GMI: Gross Margin Index
    gm = (sales - cogs) / sales if sales > 0 else 0
    gm_prev = (sales_prev - cogs_prev) / sales_prev if sales_prev > 0 else 0
    gmi = gm_prev / gm if gm > 0 else 1.0

    # AQI: Asset Quality Index
    hard_assets = current_assets + ppe + securities
    hard_assets_prev = current_assets_prev + ppe_prev + securities_prev
    aq = 1 - (hard_assets / total_assets) if total_assets > 0 else 0
    aq_prev = 1 - (hard_assets_prev / total_assets_prev) if total_assets_prev > 0 else 0
    aqi = aq / aq_prev if aq_prev != 0 else 1.0

    # SGI: Sales Growth Index
    sgi = sales / sales_prev if sales_prev > 0 else 1.0

    # DEPI: Depreciation Index
    dep_rate = depreciation / (ppe + depreciation) if (ppe + depreciation) > 0 else 0
    dep_rate_prev = depreciation_prev / (ppe_prev + depreciation_prev) if (ppe_prev + depreciation_prev) > 0 else 0
    depi = dep_rate_prev / dep_rate if dep_rate > 0 else 1.0

    # SGAI: SGA Expense Index
    sga_ratio = sga / sales if sales > 0 else 0
    sga_ratio_prev = sga_prev / sales_prev if sales_prev > 0 else 0
    sgai = sga_ratio / sga_ratio_prev if sga_ratio_prev > 0 else 1.0

    # TATA: Total Accruals to Total Assets
    tata = (income_continuing - cash_from_operations) / total_assets if total_assets > 0 else 0

    # LVGI: Leverage Index
    lev = (current_liabilities + lt_debt) / total_assets if total_assets > 0 else 0
    lev_prev = (current_liabilities_prev + lt_debt_prev) / total_assets_prev if total_assets_prev > 0 else 0
    lvgi = lev / lev_prev if lev_prev > 0 else 1.0

    score = m_score(dsri, gmi, aqi, sgi, depi, sgai, tata, lvgi)

    return {
        "dsri": dsri,
        "gmi": gmi,
        "aqi": aqi,
        "sgi": sgi,
        "depi": depi,
        "sgai": sgai,
        "tata": tata,
        "lvgi": lvgi,
        "m_score": score,
        "interpretation": interpret(score),
    }


THRESHOLD = -1.78


def interpret(score: float) -> str:
    """
    Interpret a Beneish M-Score.

    The threshold is -1.78 (Beneish 1999).

    Args:
        score: M-Score value

    Returns:
        Human-readable interpretation.
    """
    if score > THRESHOLD:
        return f"Likely Manipulator (M={score:.2f} > {THRESHOLD}) - High probability of earnings manipulation"
    else:
        return f"Unlikely Manipulator (M={score:.2f} < {THRESHOLD}) - Low probability of earnings manipulation"
