"""
financial-indicators: 120+ fundamental analysis indicators for stock evaluation.

Modules:
    - piotroski: Piotroski F-Score (0-9) financial strength indicator
    - altman: Altman Z-Score bankruptcy prediction model
    - beneish: Beneish M-Score earnings manipulation detection
    - graham: Graham Number and value investing metrics
    - dcf: Discounted Cash Flow valuation models
    - value: 28 value indicators (P/E, P/B, EV/EBITDA, etc.)
    - quality: 41 quality indicators (ROE, ROIC, margins, etc.)
    - integrity: 16 integrity indicators (debt ratios, liquidity, etc.)
    - growth: 15 growth indicators (revenue, EPS, dividend CAGR)
    - risk: 20 risk indicators (beta, volatility, drawdown, etc.)
"""

__version__ = "0.1.0"
__author__ = "Javier Sanz"
__url__ = "https://valuemarkers.com"

from . import piotroski
from . import altman
from . import beneish
from . import graham
from . import dcf
from . import value
