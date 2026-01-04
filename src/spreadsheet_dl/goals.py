"""
Backward compatibility shim for goals module.

This module has been moved to spreadsheet_dl.domains.finance.goals.
This shim provides backward compatibility for existing imports.

Implements:
    PHASE0-001: Restructure package for domain plugins
"""

# Re-export everything from the new location
from spreadsheet_dl.domains.finance.goals import (
    Debt,
    DebtPayoffMethod,
    DebtPayoffPlan,
    GoalCategory,
    GoalManager,
    GoalStatus,
    SavingsGoal,
    compare_payoff_methods,
    create_debt_payoff_plan,
    create_emergency_fund,
)

__all__ = [
    "Debt",
    "DebtPayoffMethod",
    "DebtPayoffPlan",
    "GoalCategory",
    "GoalManager",
    "GoalStatus",
    "SavingsGoal",
    "compare_payoff_methods",
    "create_debt_payoff_plan",
    "create_emergency_fund",
]
