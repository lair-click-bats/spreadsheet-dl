"""
Tests for Mechanical Engineering domain plugin.

Implements:
    REQ-C003-015: Comprehensive tests for mechanical engineering domain (95%+ coverage target)
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from spreadsheet_dl.domains.mechanical_engineering import (
    AssemblyInstructionsTemplate,
    BendingStressFormula,
    CADMetadataImporter,
    FatigueLifeFormula,
    FEAResultsImporter,
    ManufacturingSpecsTemplate,
    MaterialDatabaseImporter,
    MaterialPropertiesTemplate,
    MechanicalEngineeringDomainPlugin,
    MomentOfInertiaFormula,
    SafetyFactorFormula,
    StrainFormula,
    StressAnalysisTemplate,
    StressConcentrationFormula,
    StressFormula,
    ThermalExpansionFormula,
    ThermalStressFormula,
    ToleranceStackupTemplate,
    TorsionalStressFormula,
    YoungsModulusFormula,
)
from spreadsheet_dl.domains.mechanical_engineering.utils import (
    inch_to_mm,
    kg_to_lb,
    lb_to_kg,
    mm_to_inch,
    moment_of_inertia_circle,
    moment_of_inertia_rectangle,
    mpa_to_psi,
    polar_moment_of_inertia_circle,
    principal_stresses_2d,
    principal_stresses_3d,
    psi_to_mpa,
    section_modulus_circle,
    section_modulus_rectangle,
    von_mises_stress,
)

pytestmark = [pytest.mark.unit, pytest.mark.domain, pytest.mark.engineering]

# ============================================================================
# Plugin Tests
# ============================================================================


def test_plugin_metadata() -> None:
    """Test plugin metadata."""
    plugin = MechanicalEngineeringDomainPlugin()
    metadata = plugin.metadata

    assert metadata.name == "mechanical_engineering"
    assert metadata.version == "4.0.0"
    assert "mechanical-engineering" in metadata.tags
    assert "stress-analysis" in metadata.tags


def test_plugin_initialization() -> None:
    """Test plugin initialization."""
    plugin = MechanicalEngineeringDomainPlugin()
    plugin.initialize()

    # Verify templates registered (5 total)
    assert plugin.get_template("stress_analysis") == StressAnalysisTemplate
    assert plugin.get_template("material_properties") == MaterialPropertiesTemplate
    assert plugin.get_template("assembly_instructions") == AssemblyInstructionsTemplate
    assert plugin.get_template("tolerance_stackup") == ToleranceStackupTemplate
    assert plugin.get_template("manufacturing_specs") == ManufacturingSpecsTemplate

    # Verify formulas registered (11 total)
    assert plugin.get_formula("STRESS") == StressFormula
    assert plugin.get_formula("STRAIN") == StrainFormula
    assert plugin.get_formula("YOUNGS_MODULUS") == YoungsModulusFormula
    assert plugin.get_formula("MOMENT_OF_INERTIA") == MomentOfInertiaFormula
    assert plugin.get_formula("BENDING_STRESS") == BendingStressFormula
    assert plugin.get_formula("TORSIONAL_STRESS") == TorsionalStressFormula
    assert plugin.get_formula("THERMAL_EXPANSION") == ThermalExpansionFormula
    assert plugin.get_formula("THERMAL_STRESS") == ThermalStressFormula
    assert plugin.get_formula("FATIGUE_LIFE") == FatigueLifeFormula
    assert plugin.get_formula("SAFETY_FACTOR") == SafetyFactorFormula
    assert plugin.get_formula("STRESS_CONCENTRATION") == StressConcentrationFormula

    # Verify importers registered (3 total)
    assert plugin.get_importer("cad_metadata") == CADMetadataImporter
    assert plugin.get_importer("fea_results") == FEAResultsImporter
    assert plugin.get_importer("material_db") == MaterialDatabaseImporter


def test_plugin_validation() -> None:
    """Test plugin validation."""
    plugin = MechanicalEngineeringDomainPlugin()
    plugin.initialize()

    assert plugin.validate() is True


def test_plugin_cleanup() -> None:
    """Test plugin cleanup (should not raise)."""
    plugin = MechanicalEngineeringDomainPlugin()
    plugin.initialize()
    plugin.cleanup()  # Should not raise


# ============================================================================
# Template Tests
# ============================================================================


def test_stress_analysis_template_metadata() -> None:
    """Test StressAnalysisTemplate metadata."""
    template = StressAnalysisTemplate()
    metadata = template.metadata

    assert metadata.name == "Stress Analysis"
    assert "stress" in metadata.tags
    assert metadata.category == "mechanical_engineering"


def test_stress_analysis_template_generate() -> None:
    """Test StressAnalysisTemplate generation."""
    template = StressAnalysisTemplate(
        analysis_name="Test Analysis",
        num_load_cases=5,
        yield_strength=250.0,
    )

    builder = template.generate()
    assert builder is not None

    # Check workbook properties
    props = builder._workbook_properties
    assert "Test Analysis" in props.title


def test_stress_analysis_template_validation() -> None:
    """Test StressAnalysisTemplate validation."""
    template = StressAnalysisTemplate(num_load_cases=10)
    assert template.validate() is True

    # Invalid: zero load cases
    invalid_template = StressAnalysisTemplate(num_load_cases=0)
    assert invalid_template.validate() is False


def test_material_properties_template_metadata() -> None:
    """Test MaterialPropertiesTemplate metadata."""
    template = MaterialPropertiesTemplate()
    metadata = template.metadata

    assert metadata.name == "Material Properties Database"
    assert "materials" in metadata.tags


def test_material_properties_template_generate() -> None:
    """Test MaterialPropertiesTemplate generation."""
    template = MaterialPropertiesTemplate(
        num_materials=10,
        include_presets=True,
    )

    builder = template.generate()
    assert builder is not None


def test_material_properties_template_validation() -> None:
    """Test MaterialPropertiesTemplate validation."""
    template = MaterialPropertiesTemplate(num_materials=5)
    assert template.validate() is True


def test_assembly_instructions_template_metadata() -> None:
    """Test AssemblyInstructionsTemplate metadata."""
    template = AssemblyInstructionsTemplate()
    metadata = template.metadata

    assert metadata.name == "Assembly Instructions"
    assert "assembly" in metadata.tags


def test_assembly_instructions_template_generate() -> None:
    """Test AssemblyInstructionsTemplate generation."""
    template = AssemblyInstructionsTemplate(
        assembly_name="Motor Assembly",
        num_steps=8,
    )

    builder = template.generate()
    assert builder is not None


def test_tolerance_stackup_template_metadata() -> None:
    """Test ToleranceStackupTemplate metadata."""
    template = ToleranceStackupTemplate()
    metadata = template.metadata

    assert metadata.name == "Tolerance Stackup Analysis"
    assert "tolerance" in metadata.tags


def test_tolerance_stackup_template_generate() -> None:
    """Test ToleranceStackupTemplate generation."""
    template = ToleranceStackupTemplate(
        analysis_name="Gap Analysis",
        num_dimensions=6,
        target_dimension=10.0,
        tolerance_spec=0.5,
    )

    builder = template.generate()
    assert builder is not None


def test_manufacturing_specs_template_metadata() -> None:
    """Test ManufacturingSpecsTemplate metadata."""
    template = ManufacturingSpecsTemplate()
    metadata = template.metadata

    assert metadata.name == "Manufacturing Specifications"
    assert "manufacturing" in metadata.tags


def test_manufacturing_specs_template_generate() -> None:
    """Test ManufacturingSpecsTemplate generation."""
    template = ManufacturingSpecsTemplate(
        part_name="Shaft",
        part_number="SH-001",
        revision="B",
        num_features=10,
    )

    builder = template.generate()
    assert builder is not None


# ============================================================================
# Formula Tests
# ============================================================================


def test_stress_formula() -> None:
    """Test StressFormula."""
    formula = StressFormula()

    # Test metadata
    assert formula.metadata.name == "STRESS"
    assert len(formula.metadata.arguments) == 2

    # Test build
    result = formula.build("1000", "100")
    assert result == "1000/100"


def test_strain_formula() -> None:
    """Test StrainFormula."""
    formula = StrainFormula()

    # Test metadata
    assert formula.metadata.name == "STRAIN"

    # Test build
    result = formula.build("0.5", "100")
    assert result == "0.5/100"


def test_youngs_modulus_formula() -> None:
    """Test YoungsModulusFormula."""
    formula = YoungsModulusFormula()

    # Test metadata
    assert formula.metadata.name == "YOUNGS_MODULUS"

    # Test build
    result = formula.build("200", "0.001")
    assert result == "200/0.001"


def test_moment_of_inertia_formula() -> None:
    """Test MomentOfInertiaFormula."""
    formula = MomentOfInertiaFormula()

    # Test metadata
    assert formula.metadata.name == "MOMENT_OF_INERTIA"

    # Test build
    result = formula.build("10", "20")
    assert result == "10*POWER(20;3)/12"


def test_bending_stress_formula() -> None:
    """Test BendingStressFormula."""
    formula = BendingStressFormula()

    # Test metadata
    assert formula.metadata.name == "BENDING_STRESS"

    # Test build
    result = formula.build("1000000", "10", "6666.67")
    assert result == "1000000*10/6666.67"


def test_torsional_stress_formula() -> None:
    """Test TorsionalStressFormula."""
    formula = TorsionalStressFormula()

    # Test metadata
    assert formula.metadata.name == "TORSIONAL_STRESS"

    # Test build
    result = formula.build("500000", "10", "15707.96")
    assert result == "500000*10/15707.96"


def test_thermal_expansion_formula() -> None:
    """Test ThermalExpansionFormula."""
    formula = ThermalExpansionFormula()

    # Test metadata
    assert formula.metadata.name == "THERMAL_EXPANSION"

    # Test build
    result = formula.build("11.7e-6", "1000", "100")
    assert result == "11.7e-6*1000*100"


def test_thermal_stress_formula() -> None:
    """Test ThermalStressFormula."""
    formula = ThermalStressFormula()

    # Test metadata
    assert formula.metadata.name == "THERMAL_STRESS"

    # Test build
    result = formula.build("200000", "11.7e-6", "100")
    assert result == "200000*11.7e-6*100"


def test_fatigue_life_formula() -> None:
    """Test FatigueLifeFormula."""
    formula = FatigueLifeFormula()

    # Test metadata
    assert formula.metadata.name == "FATIGUE_LIFE"

    # Test build
    result = formula.build("1e12", "100", "3")
    assert result == "1e12/POWER(100;3)"


def test_safety_factor_formula() -> None:
    """Test SafetyFactorFormula."""
    formula = SafetyFactorFormula()

    # Test metadata
    assert formula.metadata.name == "SAFETY_FACTOR"

    # Test build
    result = formula.build("250", "100")
    assert result == "250/100"


def test_stress_concentration_formula() -> None:
    """Test StressConcentrationFormula."""
    formula = StressConcentrationFormula()

    # Test metadata
    assert formula.metadata.name == "STRESS_CONCENTRATION"

    # Test build
    result = formula.build("3.0", "50")
    assert result == "3.0*50"


def test_formula_argument_validation() -> None:
    """Test formula argument validation."""
    formula = StressFormula()

    # Valid: 2 arguments
    formula.validate_arguments(("100", "10"))

    # Invalid: too few arguments
    with pytest.raises(ValueError, match="at least 2"):
        formula.validate_arguments(("100",))

    # Invalid: too many arguments
    with pytest.raises(ValueError, match="at most 2"):
        formula.validate_arguments(("100", "10", "5"))


# ============================================================================
# Importer Tests
# ============================================================================


def test_cad_metadata_importer_metadata() -> None:
    """Test CADMetadataImporter metadata."""
    importer = CADMetadataImporter()
    metadata = importer.metadata

    assert metadata.name == "CAD Metadata Importer"
    assert "step" in metadata.supported_formats
    assert "iges" in metadata.supported_formats


def test_cad_metadata_importer_validate_source() -> None:
    """Test CADMetadataImporter source validation."""
    importer = CADMetadataImporter()

    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as f:
        temp_path = Path(f.name)

    try:
        assert importer.validate_source(temp_path) is True
        assert importer.validate_source(temp_path.with_suffix(".txt")) is False
    finally:
        temp_path.unlink()


def test_cad_metadata_importer_step() -> None:
    """Test CADMetadataImporter with STEP file."""
    importer = CADMetadataImporter()

    # Create mock STEP file
    step_content = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Test Part'),'2;1');
FILE_NAME('test_part.step','2024-01-01',('Engineer'),('Company'),'','','');
ENDSEC;
DATA;
ENDSEC;
END-ISO-10303-21;
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".step", delete=False) as f:
        f.write(step_content)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        assert len(result.data) > 0
        assert result.data[0]["format"] == "STEP"
    finally:
        temp_path.unlink()


def test_fea_results_importer_metadata() -> None:
    """Test FEAResultsImporter metadata."""
    importer = FEAResultsImporter()
    metadata = importer.metadata

    assert metadata.name == "FEA Results Importer"
    assert "csv" in metadata.supported_formats
    assert "json" in metadata.supported_formats


def test_fea_results_importer_csv() -> None:
    """Test FEAResultsImporter with CSV file."""
    importer = FEAResultsImporter()

    # Create mock FEA CSV file
    csv_content = """NodeID,X,Y,Z,StressX,StressY,VonMises,Displacement
1,0,0,0,100,50,91.85,0.5
2,1,0,0,120,60,110.22,0.6
3,2,0,0,80,40,73.48,0.4
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        assert result.records_imported == 3
        assert result.data[0]["node_id"] == 1
        assert result.data[0]["stress_vm"] == 91.85
    finally:
        temp_path.unlink()


def test_fea_results_importer_json() -> None:
    """Test FEAResultsImporter with JSON file."""
    importer = FEAResultsImporter()

    # Create mock FEA JSON file
    fea_data = {
        "nodes": [
            {
                "node_id": 1,
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "stress_x": 100.0,
                "stress_y": 50.0,
                "stress_vm": 91.85,
                "displacement": 0.5,
            },
            {
                "node_id": 2,
                "x": 1.0,
                "y": 0.0,
                "z": 0.0,
                "stress_x": 120.0,
                "stress_y": 60.0,
                "stress_vm": 110.22,
                "displacement": 0.6,
            },
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(fea_data, f)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        assert result.records_imported == 2
        assert result.data[0]["node_id"] == 1
    finally:
        temp_path.unlink()


def test_material_database_importer_metadata() -> None:
    """Test MaterialDatabaseImporter metadata."""
    importer = MaterialDatabaseImporter()
    metadata = importer.metadata

    assert metadata.name == "Material Database Importer"
    assert "csv" in metadata.supported_formats
    assert "json" in metadata.supported_formats


def test_material_database_importer_csv() -> None:
    """Test MaterialDatabaseImporter with CSV file."""
    importer = MaterialDatabaseImporter()

    # Create mock material CSV file
    csv_content = """Name,Specification,YieldStrength,UltimateStrength,YoungsModulus,PoissonsRatio,Density,CTE
Steel A36,ASTM A36,250,400,200,0.30,7850,11.7
Aluminum 6061,AA 6061-T6,276,310,68.9,0.33,2700,23.6
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        assert result.records_imported == 2
        assert result.data[0]["name"] == "Steel A36"
        assert result.data[0]["yield_strength"] == 250.0
        assert result.data[1]["name"] == "Aluminum 6061"
    finally:
        temp_path.unlink()


def test_material_database_importer_json() -> None:
    """Test MaterialDatabaseImporter with JSON file."""
    importer = MaterialDatabaseImporter()

    # Create mock material JSON file
    material_data = {
        "materials": [
            {
                "name": "Steel A36",
                "specification": "ASTM A36",
                "yield_strength": 250.0,
                "ultimate_strength": 400.0,
                "youngs_modulus": 200.0,
                "poissons_ratio": 0.30,
                "density": 7850.0,
                "cte": 11.7,
            },
            {
                "name": "Aluminum 6061",
                "specification": "AA 6061-T6",
                "yield_strength": 276.0,
                "ultimate_strength": 310.0,
                "youngs_modulus": 68.9,
                "poissons_ratio": 0.33,
                "density": 2700.0,
                "cte": 23.6,
            },
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(material_data, f)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        assert result.records_imported == 2
    finally:
        temp_path.unlink()


# ============================================================================
# Utility Function Tests
# ============================================================================


def test_unit_conversions() -> None:
    """Test unit conversion functions."""
    # Stress conversions
    assert abs(mpa_to_psi(100) - 14503.77) < 0.01
    assert abs(psi_to_mpa(14503.77) - 100.0) < 0.01

    # Length conversions
    assert abs(mm_to_inch(25.4) - 1.0) < 0.001
    assert abs(inch_to_mm(1.0) - 25.4) < 0.001

    # Mass conversions
    assert abs(kg_to_lb(1.0) - 2.20462) < 0.0001
    assert abs(lb_to_kg(2.20462) - 1.0) < 0.0001


def test_von_mises_stress() -> None:
    """Test von Mises stress calculation."""
    # Test 2D case: sigma_x=100, sigma_y=50, tau_xy=25
    # von Mises = sqrt(100^2 + 50^2 - 100*50 + 3*25^2) = 96.82
    vm = von_mises_stress(100, 50, 0, 25)
    assert abs(vm - 96.82) < 0.1

    # Test pure tension
    vm_tension = von_mises_stress(100, 0, 0, 0)
    assert abs(vm_tension - 100.0) < 0.01


def test_principal_stresses_2d() -> None:
    """Test 2D principal stress calculation."""
    # sigma_x=100, sigma_y=50, tau_xy=25
    # avg = 75, radius = sqrt(25^2 + 25^2) = 35.36
    # sigma_1 = 110.36, sigma_2 = 39.64
    sigma_1, sigma_2 = principal_stresses_2d(100, 50, 25)

    assert sigma_1 > sigma_2  # sigma_1 is max
    assert abs(sigma_1 - 110.36) < 0.1
    assert abs(sigma_2 - 39.64) < 0.1


def test_principal_stresses_3d() -> None:
    """Test 3D principal stress calculation."""
    # Pure normal stresses (no shear)
    sigma_1, sigma_2, sigma_3 = principal_stresses_3d(100, 50, 25, 0, 0, 0)

    assert sigma_1 == 100.0  # Max
    assert sigma_2 == 50.0  # Middle
    assert sigma_3 == 25.0  # Min


def test_moment_of_inertia_rectangle_calc() -> None:
    """Test rectangular moment of inertia calculation."""
    inertia = moment_of_inertia_rectangle(10, 20)
    expected = (10 * 20**3) / 12.0
    assert abs(inertia - expected) < 0.01


def test_moment_of_inertia_circle_calc() -> None:
    """Test circular moment of inertia calculation."""
    inertia = moment_of_inertia_circle(10)
    assert inertia > 0  # Just check it's positive


def test_polar_moment_of_inertia_circle_calc() -> None:
    """Test polar moment of inertia calculation."""
    J = polar_moment_of_inertia_circle(10)
    assert J > 0  # Just check it's positive


def test_section_modulus_calculations() -> None:
    """Test section modulus calculations."""
    S_rect = section_modulus_rectangle(10, 20)
    assert S_rect > 0

    S_circ = section_modulus_circle(10)
    assert S_circ > 0


# ============================================================================
# Integration Tests
# ============================================================================


def test_full_plugin_workflow() -> None:
    """Test complete plugin workflow."""
    # Initialize plugin
    plugin = MechanicalEngineeringDomainPlugin()
    plugin.initialize()

    # Get template and generate
    template_class = plugin.get_template("stress_analysis")
    assert template_class is not None

    template = template_class(analysis_name="Integration Test")
    builder = template.generate()
    assert builder is not None

    # Validate and cleanup
    assert plugin.validate() is True
    plugin.cleanup()


def test_template_with_builder_integration() -> None:
    """Test template integration with SpreadsheetBuilder."""
    template = StressAnalysisTemplate(
        analysis_name="Builder Test",
        num_load_cases=3,
    )

    builder = template.generate()
    assert builder is not None

    # Verify builder has content
    assert len(builder._sheets) > 0


# ============================================================================
# Additional Coverage Tests
# ============================================================================


def test_cad_metadata_importer_iges() -> None:
    """Test CADMetadataImporter with IGES file."""
    importer = CADMetadataImporter()

    # Create mock IGES file
    iges_content = """                                                                        S      1
IGES test file                                                          S      2
1H,,1H;,7Htest.ig,11HTest Author,10HCompany XY,                        G      1
15H2024-01-01,1.,1,4HMM,1,0.01,15H20240101.120000,,,;                  G      2
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".igs", delete=False) as f:
        f.write(iges_content)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        assert len(result.data) > 0
        assert result.data[0]["format"] == "IGES"
    finally:
        temp_path.unlink()


def test_fea_results_importer_invalid_file() -> None:
    """Test FEAResultsImporter with invalid file."""
    importer = FEAResultsImporter()

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is False
        assert len(result.errors) > 0
    finally:
        temp_path.unlink()


def test_material_database_importer_missing_name() -> None:
    """Test MaterialDatabaseImporter with missing material name."""
    importer = MaterialDatabaseImporter()

    # Create CSV with missing name
    csv_content = """Name,YieldStrength
,250
Steel,300
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_path = Path(f.name)

    try:
        result = importer.import_data(temp_path)
        assert result.success is True
        # Should skip row with missing name
        assert result.records_imported == 1
        assert len(result.warnings) > 0
    finally:
        temp_path.unlink()


def test_principal_stresses_3d_with_shear() -> None:
    """Test 3D principal stress calculation with shear stresses."""
    sigma_1, _sigma_2, sigma_3 = principal_stresses_3d(
        100, 50, 25, tau_xy=10, tau_yz=5, tau_xz=5
    )

    # With shear, uses approximation
    assert sigma_1 > 0
    assert sigma_3 <= min(100, 50, 25)


def test_assembly_instructions_validation() -> None:
    """Test AssemblyInstructionsTemplate validation."""
    template = AssemblyInstructionsTemplate(num_steps=5, assembly_name="Test")
    assert template.validate() is True

    # Invalid: zero steps
    invalid = AssemblyInstructionsTemplate(num_steps=0)
    assert invalid.validate() is False

    # Invalid: empty name
    invalid2 = AssemblyInstructionsTemplate(assembly_name="")
    assert invalid2.validate() is False


def test_tolerance_stackup_validation() -> None:
    """Test ToleranceStackupTemplate validation."""
    template = ToleranceStackupTemplate(num_dimensions=5, tolerance_spec=0.1)
    assert template.validate() is True

    # Invalid: zero spec
    invalid = ToleranceStackupTemplate(tolerance_spec=0)
    assert invalid.validate() is False


def test_manufacturing_specs_validation() -> None:
    """Test ManufacturingSpecsTemplate validation."""
    template = ManufacturingSpecsTemplate(
        part_name="Shaft", part_number="SH-001", num_features=5
    )
    assert template.validate() is True

    # Invalid: empty part name
    invalid = ManufacturingSpecsTemplate(part_name="", part_number="SH-001")
    assert invalid.validate() is False

    # Invalid: empty part number
    invalid2 = ManufacturingSpecsTemplate(part_name="Shaft", part_number="")
    assert invalid2.validate() is False
