"""
Biology Domain Plugin for SpreadsheetDL.

Implements:
    TASK-C006: Biology domain plugin
    PHASE-C: Domain plugin implementations

Provides biology-specific functionality including:
- Lab experiment protocols and plate reader data templates
- Gene expression and sequencing results templates
- Molecular biology and biochemistry formulas
- FASTA, GenBank, and plate reader importers
- Ecology statistics and population growth calculations

Features:
    - 5 professional templates for research workflows
    - 12 specialized formulas for biology calculations
    - 3 importers for biological data formats
    - Integration with lab instruments and sequence databases
"""

from __future__ import annotations

from spreadsheet_dl.domains.biology.plugin import BiologyDomainPlugin

__all__ = [
    "BiologyDomainPlugin",
]
