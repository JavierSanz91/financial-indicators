"""
Altman Z-Score: Bankruptcy prediction model.

Developed by Edward Altman at NYU Stern (1968).
Predicts the probability of corporate bankruptcy within 2 years.

Reference:
    Altman, E.I. (1968). "Financial Ratios, Discriminant Analysis and the
    Prediction of Corporate Bankruptcy." Journal of Finance, 23(4), 589-609.
"""


def z_score(
    working_capital: float,
    total_assets: float,
    retained_earnings: float,
    ebit: float,
    market_cap: float,
    total_liabilities: float,
    revenue: float,
) -> float:
    """
    Calculate the Altman Z-Score for manufacturing/public companies.

    Formula: Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5

    Where:
        X1 = Working Capital / Total Assets
        X2 = Retained Earnings / Total Assets
        X3 = EBIT / Total Assets
        X4 = Market Cap / Total Liabilities
        X5 = Revenue / Total Assets

    Args:
        working_capital: Current Assets - Current Liabilities
        total_assets: Total Assets
        retained_earnings: Retained Earnings
        ebit: Earnings Before Interest and Taxes
        market_cap: Market Capitalization (equity market value)
        total_liabilities: Total Liabilities
        revenue: Total Revenue / Sales

    Returns:
        Z-Score float value.
        > 2.99: Safe Zone (low bankruptcy risk)
        1.81-2.99: Grey Zone (moderate risk)
        < 1.81: Distress Zone (high bankruptcy risk)
    """
    if total_assets == 0 or total_liabilities == 0:
        return 0.0

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = market_cap / total_liabilities
    x5 = revenue / total_assets

    return 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5


def z_score_private(
    working_capital: float,
    total_assets: float,
    retained_earnings: float,
    ebit: float,
    book_value_equity: float,
    total_liabilities: float,
    revenue: float,
) -> float:
    """
    Altman Z'-Score for private (non-public) companies.

    Uses book value of equity instead of market cap.
    Formula: Z' = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998*X5

    Returns:
        Z'-Score. Thresholds: > 2.90 safe, 1.23-2.90 grey, < 1.23 distress.
    """
    if total_assets == 0 or total_liabilities == 0:
        return 0.0

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = book_value_equity / total_liabilities
    x5 = revenue / total_assets

    return 0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.420 * x4 + 0.998 * x5


def z_score_non_manufacturing(
    working_capital: float,
    total_assets: float,
    retained_earnings: float,
    ebit: float,
    market_cap: float,
    total_liabilities: float,
) -> float:
    """
    Altman Z''-Score for non-manufacturing and emerging market companies.

    Removes revenue/assets ratio (X5) which is industry-sensitive.
    Formula: Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4

    Returns:
        Z''-Score. Thresholds: > 2.60 safe, 1.10-2.60 grey, < 1.10 distress.
    """
    if total_assets == 0 or total_liabilities == 0:
        return 0.0

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = market_cap / total_liabilities

    return 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4


def interpret(z: float, model: str = "original") -> str:
    """
    Interpret an Altman Z-Score.

    Args:
        z: Z-Score value
        model: "original" (public mfg), "private", or "non_manufacturing"

    Returns:
        Human-readable interpretation with zone classification.
    """
    thresholds = {
        "original": (2.99, 1.81),
        "private": (2.90, 1.23),
        "non_manufacturing": (2.60, 1.10),
    }

    safe, distress = thresholds.get(model, (2.99, 1.81))

    if z > safe:
        return f"Safe Zone (Z={z:.2f}) - Low probability of bankruptcy"
    elif z > distress:
        return f"Grey Zone (Z={z:.2f}) - Moderate risk, further analysis needed"
    else:
        return f"Distress Zone (Z={z:.2f}) - High probability of financial distress"
