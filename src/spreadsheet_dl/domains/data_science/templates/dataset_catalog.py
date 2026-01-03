"""
Dataset Catalog Template for data inventory management.

Implements:
    TASK-C001: DatasetCatalogTemplate for data science domain
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spreadsheet_dl.domains.base import BaseTemplate, TemplateMetadata

if TYPE_CHECKING:
    from spreadsheet_dl.builder import SpreadsheetBuilder


@dataclass
class DatasetCatalogTemplate(BaseTemplate):
    """
    Dataset catalog and inventory template.

    Implements:
        TASK-C001: DatasetCatalogTemplate with dataset metadata and statistics

    Features:
    - Dataset name and source tracking
    - Date added timestamp
    - Size metrics (rows/columns)
    - Schema information (data types)
    - Statistical summaries (mean/std)
    - Storage location
    - Description field
    - Summary row with total counts
    - Data type breakdown chart

    Example:
        >>> template = DatasetCatalogTemplate(
        ...     organization="Acme Corp",
        ...     include_chart=True,
        ... )
        >>> builder = template.generate()
        >>> builder.save("dataset_catalog.ods")
    """

    organization: str = "Data Science Team"
    include_chart: bool = True
    theme: str = "default"

    @property
    def metadata(self) -> TemplateMetadata:
        """
        Get template metadata.

        Returns:
            TemplateMetadata for dataset catalog template

        Implements:
            TASK-C001: Template metadata
        """
        return TemplateMetadata(
            name="Dataset Catalog",
            description="Dataset inventory with metadata and statistics",
            category="data_science",
            tags=("datasets", "catalog", "inventory", "metadata"),
            version="1.0.0",
            author="SpreadsheetDL Team",
        )

    def generate(self) -> SpreadsheetBuilder:
        """
        Generate the dataset catalog spreadsheet.

        Returns:
            Configured SpreadsheetBuilder instance

        Implements:
            TASK-C001: DatasetCatalogTemplate generation
        """
        from spreadsheet_dl.builder import SpreadsheetBuilder

        builder = SpreadsheetBuilder(theme=self.theme)

        # Set workbook properties
        builder.workbook_properties(
            title=f"Dataset Catalog - {self.organization}",
            author=self.organization,
            subject="Dataset Inventory",
            description=f"Dataset catalog and metadata for {self.organization}",
            keywords=["datasets", "catalog", "metadata", "inventory"],
        )

        # Create catalog sheet
        builder.sheet("Datasets")

        # Define columns
        builder.column("Dataset Name", width="200pt", style="text")
        builder.column("Source", width="150pt", style="text")
        builder.column("Date Added", width="100pt", type="date")
        builder.column("Rows", width="80pt", type="number")
        builder.column("Columns", width="80pt", type="number")
        builder.column("Schema", width="200pt", style="text")
        builder.column("Mean", width="100pt", type="number")
        builder.column("Std Dev", width="100pt", type="number")
        builder.column("Location", width="250pt", style="text")
        builder.column("Description", width="300pt", style="text")

        # Freeze header row
        builder.freeze(rows=1)

        # Header row
        builder.row(style="header_primary")
        builder.cell("Dataset Name")
        builder.cell("Source")
        builder.cell("Date Added")
        builder.cell("Rows")
        builder.cell("Columns")
        builder.cell("Schema")
        builder.cell("Mean")
        builder.cell("Std Dev")
        builder.cell("Location")
        builder.cell("Description")

        # Add sample data
        self._add_sample_datasets(builder)

        # Add summary row
        self._add_summary_row(builder)

        # Create statistics sheet
        builder.sheet("Statistics")
        self._create_statistics_sheet(builder)

        return builder

    def _add_sample_datasets(self, builder: SpreadsheetBuilder) -> None:
        """Add sample dataset entries."""
        sample_datasets = [
            {
                "name": "Customer Transactions 2024",
                "source": "Production DB",
                "date": "2024-01-10",
                "rows": 1250000,
                "cols": 15,
                "schema": "int64(4), float64(6), object(5)",
                "mean": 125.67,
                "std": 45.23,
                "location": "s3://data-lake/customers/transactions_2024.parquet",
                "desc": "Transaction history for Q1 2024",
            },
            {
                "name": "Product Catalog",
                "source": "API Export",
                "date": "2024-01-15",
                "rows": 5000,
                "cols": 25,
                "schema": "int64(3), float64(5), object(17)",
                "mean": 89.50,
                "std": 120.45,
                "location": "/data/products/catalog_v2.csv",
                "desc": "Complete product catalog with pricing and inventory",
            },
            {
                "name": "User Behavior Logs",
                "source": "Analytics Platform",
                "date": "2024-01-20",
                "rows": 8500000,
                "cols": 20,
                "schema": "int64(5), float64(8), object(7)",
                "mean": 2.45,
                "std": 1.89,
                "location": "s3://analytics/events/user_behavior_jan.parquet",
                "desc": "User interaction events and clickstream data",
            },
            {
                "name": "Weather Station Readings",
                "source": "IoT Sensors",
                "date": "2024-01-25",
                "rows": 2160000,
                "cols": 12,
                "schema": "int64(2), float64(9), datetime64(1)",
                "mean": 18.7,
                "std": 5.2,
                "location": "/data/weather/readings_2024_q1.csv",
                "desc": "Hourly temperature, humidity, and pressure readings",
            },
        ]

        for ds in sample_datasets:
            builder.row()
            builder.cell(ds["name"])
            builder.cell(ds["source"])
            builder.cell(ds["date"])
            builder.cell(ds["rows"])
            builder.cell(ds["cols"])
            builder.cell(ds["schema"])
            builder.cell(ds["mean"])
            builder.cell(ds["std"])
            builder.cell(ds["location"])
            builder.cell(ds["desc"])

    def _add_summary_row(self, builder: SpreadsheetBuilder) -> None:
        """Add summary row with totals."""
        builder.row(style="header_secondary")
        builder.cell("TOTAL DATASETS")
        builder.cell("=COUNTA(A2:A5)")  # Count non-empty cells in name column
        builder.cell("")  # Date column
        builder.cell("=SUM(D2:D5)")  # Total rows
        builder.cell("")  # Columns
        builder.cell("")  # Schema
        builder.cell("=AVERAGE(G2:G5)")  # Average mean
        builder.cell("=AVERAGE(H2:H5)")  # Average std
        builder.cell("")  # Location
        builder.cell("")  # Description

    def _create_statistics_sheet(self, builder: SpreadsheetBuilder) -> None:
        """Create dataset statistics summary sheet."""
        builder.column("Metric", width="200pt", style="text")
        builder.column("Value", width="120pt", type="number")

        builder.freeze(rows=1)

        # Header
        builder.row(style="header_primary")
        builder.cell("Metric")
        builder.cell("Value")

        # Statistics
        stats = [
            ("Total Datasets", "=COUNTA(Datasets.A2:Datasets.A100)"),
            ("Total Data Points", "=SUM(Datasets.D2:Datasets.D100)"),
            ("Average Dataset Size (rows)", "=AVERAGE(Datasets.D2:Datasets.D100)"),
            ("Average Columns", "=AVERAGE(Datasets.E2:Datasets.E100)"),
            ("Total Storage Items", "=COUNTA(Datasets.I2:Datasets.I100)"),
        ]

        for stat_name, formula in stats:
            builder.row()
            builder.cell(stat_name)
            builder.cell(formula)


__all__ = ["DatasetCatalogTemplate"]
