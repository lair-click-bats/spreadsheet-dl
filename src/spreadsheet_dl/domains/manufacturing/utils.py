"""
Manufacturing domain utility functions.

Implements:
    TASK-C005: Manufacturing utility functions
"""

from __future__ import annotations

from typing import Any


def calculate_oee(availability: float, performance: float, quality: float) -> float:
    """
    Calculate Overall Equipment Effectiveness (OEE).

    Implements:
        TASK-C005: OEE calculation utility

    Args:
        availability: Availability percentage (0-100)
        performance: Performance percentage (0-100)
        quality: Quality percentage (0-100)

    Returns:
        OEE percentage (0-100)

    Example:
        >>> oee = calculate_oee(95.0, 98.0, 99.5)
        >>> # Returns: 92.621 (95% * 98% * 99.5%)
    """
    return (availability / 100) * (performance / 100) * (quality / 100) * 100


def calculate_defect_rate(defects: int, total: int) -> float:
    """
    Calculate defect rate percentage.

    Implements:
        TASK-C005: Defect rate calculation

    Args:
        defects: Number of defective units
        total: Total number of units inspected

    Returns:
        Defect rate percentage

    Example:
        >>> rate = calculate_defect_rate(25, 1000)
        >>> # Returns: 2.5
    """
    if total == 0:
        return 0.0
    return (defects / total) * 100


def calculate_first_pass_yield(good_units: int, total_units: int) -> float:
    """
    Calculate first pass yield percentage.

    Implements:
        TASK-C005: First pass yield calculation

    Args:
        good_units: Number of units passing first inspection
        total_units: Total number of units produced

    Returns:
        First pass yield percentage

    Example:
        >>> fpy = calculate_first_pass_yield(950, 1000)
        >>> # Returns: 95.0
    """
    if total_units == 0:
        return 0.0
    return (good_units / total_units) * 100


def calculate_cycle_time(production_time: float, units_produced: int) -> float:
    """
    Calculate manufacturing cycle time.

    Implements:
        TASK-C005: Cycle time calculation

    Args:
        production_time: Total production time in minutes
        units_produced: Number of units produced

    Returns:
        Cycle time in minutes per unit

    Example:
        >>> cycle_time = calculate_cycle_time(480, 120)
        >>> # Returns: 4.0 (4 minutes per unit)
    """
    if units_produced == 0:
        return 0.0
    return production_time / units_produced


def calculate_takt_time(available_time: float, demand: int) -> float:
    """
    Calculate takt time.

    Implements:
        TASK-C005: Takt time calculation

    Args:
        available_time: Available production time in seconds
        demand: Customer demand in units

    Returns:
        Takt time in seconds per unit

    Example:
        >>> takt = calculate_takt_time(28800, 1200)
        >>> # Returns: 24.0 (24 seconds per unit)
    """
    if demand == 0:
        return 0.0
    return available_time / demand


def calculate_eoq(
    annual_demand: float, order_cost: float, holding_cost: float
) -> float:
    """
    Calculate Economic Order Quantity.

    Implements:
        TASK-C005: EOQ calculation

    Args:
        annual_demand: Annual demand in units
        order_cost: Cost per order
        holding_cost: Annual holding cost per unit

    Returns:
        Economic order quantity

    Example:
        >>> eoq = calculate_eoq(10000, 50, 5)
        >>> # Returns: 447.21 (approximately)
    """
    if holding_cost == 0:
        return 0.0
    return float(((2 * annual_demand * order_cost) / holding_cost) ** 0.5)


def calculate_reorder_point(
    demand_rate: float, lead_time: float, safety_stock: float
) -> float:
    """
    Calculate inventory reorder point.

    Implements:
        TASK-C005: Reorder point calculation

    Args:
        demand_rate: Average daily demand
        lead_time: Lead time in days
        safety_stock: Safety stock quantity

    Returns:
        Reorder point quantity

    Example:
        >>> rop = calculate_reorder_point(50, 7, 100)
        >>> # Returns: 450.0
    """
    return (demand_rate * lead_time) + safety_stock


def calculate_safety_stock(
    z_score: float, demand_stddev: float, lead_time: float
) -> float:
    """
    Calculate safety stock quantity.

    Implements:
        TASK-C005: Safety stock calculation

    Args:
        z_score: Z-score for desired service level (e.g., 1.65 for 95%)
        demand_stddev: Standard deviation of demand
        lead_time: Lead time in days

    Returns:
        Safety stock quantity

    Example:
        >>> safety = calculate_safety_stock(1.65, 15, 7)
        >>> # Returns: 65.45 (approximately)
    """
    return float(z_score * demand_stddev * (lead_time**0.5))


def parse_manufacturing_date(date_str: str) -> str:
    """
    Parse various manufacturing date formats to ISO format.

    Implements:
        TASK-C005: Date parsing utility

    Args:
        date_str: Date string in various formats

    Returns:
        ISO format date string (YYYY-MM-DD)

    Example:
        >>> iso_date = parse_manufacturing_date("12/25/2024")
        >>> # Returns: "2024-12-25"
    """
    from datetime import datetime

    # Common manufacturing date formats
    formats = [
        "%Y-%m-%d",  # ISO
        "%m/%d/%Y",  # US
        "%d/%m/%Y",  # EU
        "%Y/%m/%d",  # Asian
        "%d.%m.%Y",  # German
        "%d-%m-%Y",  # UK
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # If all fail, return original
    return date_str


def format_manufacturing_number(value: Any, decimals: int = 2) -> str:
    """
    Format number for manufacturing reports.

    Implements:
        TASK-C005: Number formatting utility

    Args:
        value: Numeric value to format
        decimals: Number of decimal places

    Returns:
        Formatted number string

    Example:
        >>> formatted = format_manufacturing_number(1234.5678)
        >>> # Returns: "1,234.57"
    """
    try:
        num = float(value)
        return f"{num:,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


__all__ = [
    "calculate_cycle_time",
    "calculate_defect_rate",
    "calculate_eoq",
    "calculate_first_pass_yield",
    "calculate_oee",
    "calculate_reorder_point",
    "calculate_safety_stock",
    "calculate_takt_time",
    "format_manufacturing_number",
    "parse_manufacturing_date",
]
