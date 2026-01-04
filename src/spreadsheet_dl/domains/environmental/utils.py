"""
Environmental domain utility functions.

Implements:
    TASK-C008: Environmental domain utilities

Provides helper functions for environmental calculations,
unit conversions, and data processing.
"""

from __future__ import annotations

import math
from typing import Sequence

# Molecular weights for unit conversions (g/mol)
MOLECULAR_WEIGHTS = {
    "O3": 48.0,
    "NO2": 46.0,
    "SO2": 64.1,
    "CO": 28.0,
}

# Standard conditions for gas conversion
STANDARD_TEMP_K = 298.15  # 25 C
STANDARD_PRESSURE_KPA = 101.325  # 1 atm


def ppm_to_ugm3(ppm: float, molecular_weight: float) -> float:
    """
    Convert gas concentration from ppm to ug/m3.

    Args:
        ppm: Concentration in parts per million
        molecular_weight: Molecular weight of gas (g/mol)

    Returns:
        Concentration in micrograms per cubic meter

    Implements:
        TASK-C008: Unit conversion for air quality

    Example:
        >>> ppm_to_ugm3(0.1, 48.0)  # O3
        196.1...
    """
    # ug/m3 = ppm * MW * 1000 / (24.45)
    # 24.45 is molar volume at 25C, 1atm
    return ppm * molecular_weight * 1000 / 24.45


def ugm3_to_ppm(ugm3: float, molecular_weight: float) -> float:
    """
    Convert gas concentration from ug/m3 to ppm.

    Args:
        ugm3: Concentration in micrograms per cubic meter
        molecular_weight: Molecular weight of gas (g/mol)

    Returns:
        Concentration in parts per million

    Implements:
        TASK-C008: Unit conversion for air quality

    Example:
        >>> ugm3_to_ppm(196.0, 48.0)  # O3
        0.0999...
    """
    return ugm3 * 24.45 / (molecular_weight * 1000)


def calculate_aqi(pm25: float) -> int:
    """
    Calculate Air Quality Index from PM2.5 concentration.

    Args:
        pm25: PM2.5 concentration in ug/m3

    Returns:
        AQI value (0-500+)

    Implements:
        TASK-C008: AQI calculation utility

    Example:
        >>> calculate_aqi(35.5)
        100
    """
    # EPA AQI breakpoints for PM2.5 (24-hour average)
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]

    for bp_lo, bp_hi, i_lo, i_hi in breakpoints:
        if bp_lo <= pm25 <= bp_hi:
            # Linear interpolation
            aqi = ((i_hi - i_lo) / (bp_hi - bp_lo)) * (pm25 - bp_lo) + i_lo
            return int(round(aqi))

    # Above highest breakpoint
    if pm25 > 500.4:
        return 500

    return 0


def calculate_wqi(
    do_saturation: float,
    bod: float,
    ph: float,
    turbidity: float = 0,
) -> float:
    """
    Calculate Water Quality Index (simplified).

    Args:
        do_saturation: Dissolved oxygen saturation (%)
        bod: Biochemical oxygen demand (mg/L)
        ph: pH value
        turbidity: Turbidity (NTU, optional)

    Returns:
        WQI score (0-100)

    Implements:
        TASK-C008: WQI calculation utility

    Example:
        >>> calculate_wqi(95, 2, 7.2)
        87.0
    """
    # DO sub-index: 100 at 100% saturation
    do_index = min(do_saturation, 100)

    # BOD sub-index: 100 at 0, decreasing
    bod_index = max(0, 100 - bod * 10)

    # pH sub-index: 100 at pH 7, decreasing away
    ph_index = max(0, 100 - abs(ph - 7) * 15)

    if turbidity > 0:
        turb_index = max(0, 100 - turbidity * 2)
        return (do_index + bod_index + ph_index + turb_index) / 4
    else:
        return (do_index + bod_index + ph_index) / 3


def calculate_bod(
    initial_do: float,
    final_do: float,
    sample_volume: float,
    bottle_volume: float = 300,
) -> float:
    """
    Calculate Biochemical Oxygen Demand.

    Args:
        initial_do: Initial dissolved oxygen (mg/L)
        final_do: Final dissolved oxygen (mg/L)
        sample_volume: Sample volume (mL)
        bottle_volume: BOD bottle volume (mL, default 300)

    Returns:
        BOD value (mg/L)

    Implements:
        TASK-C008: BOD calculation utility

    Example:
        >>> calculate_bod(8.5, 3.2, 30)
        53.0
    """
    return (initial_do - final_do) * (bottle_volume / sample_volume)


def calculate_shannon_diversity(counts: Sequence[int | float]) -> float:
    """
    Calculate Shannon Diversity Index.

    Args:
        counts: Sequence of species counts

    Returns:
        Shannon diversity index (H')

    Implements:
        TASK-C008: Shannon diversity calculation

    Example:
        >>> calculate_shannon_diversity([10, 10, 10, 10])
        1.386...
    """
    total = sum(counts)
    if total == 0:
        return 0.0

    h_prime = 0.0
    for count in counts:
        if count > 0:
            p_i = count / total
            h_prime -= p_i * math.log(p_i)

    return h_prime


def calculate_simpson_index(counts: Sequence[int | float]) -> float:
    """
    Calculate Simpson's Diversity Index (1-D).

    Args:
        counts: Sequence of species counts

    Returns:
        Simpson's diversity index (1-D)

    Implements:
        TASK-C008: Simpson index calculation

    Example:
        >>> calculate_simpson_index([10, 10, 10, 10])
        0.75
    """
    total = sum(counts)
    if total == 0:
        return 0.0

    d = 0.0
    for count in counts:
        p_i = count / total
        d += p_i * p_i

    return 1 - d


def calculate_carbon_equivalent(
    amount: float,
    gas_type: str = "co2",
) -> float:
    """
    Convert emissions to CO2 equivalent.

    Args:
        amount: Emission amount (kg or tonnes)
        gas_type: Gas type (co2, ch4, n2o, hfc, pfc, sf6)

    Returns:
        CO2 equivalent

    Implements:
        TASK-C008: Carbon equivalent calculation

    Example:
        >>> calculate_carbon_equivalent(100, "ch4")
        2800.0
    """
    gwp_map = {
        "co2": 1,
        "ch4": 28,
        "n2o": 265,
        "hfc": 1430,
        "pfc": 6630,
        "sf6": 23500,
    }

    gwp = gwp_map.get(gas_type.lower(), 1)
    return amount * gwp


def calculate_ecological_footprint(
    carbon_kg: float,
    food_factor: float = 0,
    housing_m2: float = 0,
) -> float:
    """
    Calculate ecological footprint in global hectares.

    Args:
        carbon_kg: Annual CO2 emissions (kg)
        food_factor: Food consumption factor (optional)
        housing_m2: Housing area in square meters (optional)

    Returns:
        Ecological footprint (global hectares)

    Implements:
        TASK-C008: Ecological footprint calculation

    Example:
        >>> calculate_ecological_footprint(5000)
        1.35
    """
    # Carbon: 1 tonne CO2 = ~0.27 gha
    carbon_gha = (carbon_kg / 1000) * 0.27

    footprint = carbon_gha

    if food_factor > 0:
        footprint += food_factor * 0.8

    if housing_m2 > 0:
        footprint += housing_m2 * 0.0001

    return footprint


def format_concentration(
    value: float,
    unit: str = "ug/m3",
    decimals: int = 1,
) -> str:
    """
    Format concentration value with unit.

    Args:
        value: Concentration value
        unit: Unit string
        decimals: Number of decimal places

    Returns:
        Formatted concentration string

    Implements:
        TASK-C008: Concentration formatting

    Example:
        >>> format_concentration(35.56, "ug/m3", 1)
        '35.6 ug/m3'
    """
    return f"{value:.{decimals}f} {unit}"


__all__ = [
    "calculate_aqi",
    "calculate_bod",
    "calculate_carbon_equivalent",
    "calculate_ecological_footprint",
    "calculate_shannon_diversity",
    "calculate_simpson_index",
    "calculate_wqi",
    "format_concentration",
    "ppm_to_ugm3",
    "ugm3_to_ppm",
]
