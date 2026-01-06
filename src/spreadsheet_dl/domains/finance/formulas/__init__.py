"""Financial formulas for time value of money, investments, and analysis."""

from __future__ import annotations

from spreadsheet_dl.domains.finance.formulas.depreciation import (
    DecliningBalanceDepreciation,
    StraightLineDepreciation,
    SUMYearsDigitsDepreciation,
)
from spreadsheet_dl.domains.finance.formulas.investments import (
    CompoundAnnualGrowthRate,
    CompoundInterest,
    PortfolioBeta,
    ReturnOnInvestment,
    SharpeRatio,
)
from spreadsheet_dl.domains.finance.formulas.time_value import (
    FutureValue,
    InternalRateOfReturn,
    NetPresentValue,
    PaymentFormula,
    PeriodsFormula,
    PresentValue,
    RateFormula,
)

__all__ = [
    "CompoundAnnualGrowthRate",
    "CompoundInterest",
    "DecliningBalanceDepreciation",
    "FutureValue",
    "InternalRateOfReturn",
    "NetPresentValue",
    "PaymentFormula",
    "PeriodsFormula",
    "PortfolioBeta",
    "PresentValue",
    "RateFormula",
    "ReturnOnInvestment",
    "SUMYearsDigitsDepreciation",
    "SharpeRatio",
    "StraightLineDepreciation",
]
