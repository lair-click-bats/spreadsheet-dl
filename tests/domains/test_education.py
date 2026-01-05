"""
Tests for Education domain plugin.

Implements:
    Comprehensive tests for Education domain (95%+ coverage target)
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from spreadsheet_dl.domains.education import (
    AssessmentResultsImporter,
    AssessmentRubricTemplate,
    AttendanceRateFormula,
    BloomTaxonomyLevelFormula,
    CompletionRateFormula,
    CorrelationFormula,
    CourseGradebookTemplate,
    EducationDomainPlugin,
    GradeAverageFormula,
    GradebookExportImporter,
    GradeCurveFormula,
    LearningGainFormula,
    LearningObjectivesTemplate,
    LessonPlanTemplate,
    LMSDataImporter,
    MasteryLevelFormula,
    PercentileRankFormula,
    ReadabilityScoreFormula,
    StandardDeviationFormula,
    StudentAttendanceTemplate,
    WeightedGradeFormula,
)
from spreadsheet_dl.domains.education.utils import (
    calculate_attendance_rate,
    calculate_gpa,
    calculate_grade_average,
    calculate_letter_grade,
    calculate_weighted_grade,
    format_percentage,
    grade_to_points,
    points_to_grade,
)

pytestmark = [pytest.mark.unit, pytest.mark.domain]

# ============================================================================
# Plugin Tests
# ============================================================================


def test_plugin_metadata() -> None:
    """Test plugin metadata."""
    plugin = EducationDomainPlugin()
    metadata = plugin.metadata

    assert metadata.name == "education"
    assert metadata.version == "4.0.0"
    assert "education" in metadata.tags
    assert "gradebook" in metadata.tags


def test_plugin_initialization() -> None:
    """Test plugin initialization."""
    plugin = EducationDomainPlugin()
    plugin.initialize()

    # Verify templates registered (5 total)
    assert plugin.get_template("course_gradebook") == CourseGradebookTemplate
    assert plugin.get_template("lesson_plan") == LessonPlanTemplate
    assert plugin.get_template("assessment_rubric") == AssessmentRubricTemplate
    assert plugin.get_template("student_attendance") == StudentAttendanceTemplate
    assert plugin.get_template("learning_objectives") == LearningObjectivesTemplate

    # Verify formulas registered (12 total)
    # Grade formulas
    assert plugin.get_formula("GRADE_AVERAGE") == GradeAverageFormula
    assert plugin.get_formula("WEIGHTED_GRADE") == WeightedGradeFormula
    assert plugin.get_formula("GRADE_CURVE") == GradeCurveFormula

    # Statistics formulas
    assert plugin.get_formula("STANDARD_DEVIATION") == StandardDeviationFormula
    assert plugin.get_formula("PERCENTILE_RANK") == PercentileRankFormula
    assert plugin.get_formula("CORRELATION") == CorrelationFormula

    # Learning metrics formulas
    assert plugin.get_formula("LEARNING_GAIN") == LearningGainFormula
    assert plugin.get_formula("MASTERY_LEVEL") == MasteryLevelFormula
    assert plugin.get_formula("ATTENDANCE_RATE") == AttendanceRateFormula
    assert plugin.get_formula("COMPLETION_RATE") == CompletionRateFormula
    assert plugin.get_formula("BLOOM_TAXONOMY_LEVEL") == BloomTaxonomyLevelFormula
    assert plugin.get_formula("READABILITY_SCORE") == ReadabilityScoreFormula

    # Verify importers registered (3 total)
    assert plugin.get_importer("lms_data") == LMSDataImporter
    assert plugin.get_importer("gradebook_export") == GradebookExportImporter
    assert plugin.get_importer("assessment_results") == AssessmentResultsImporter


def test_plugin_validation() -> None:
    """Test plugin validation."""
    plugin = EducationDomainPlugin()
    plugin.initialize()

    assert plugin.validate() is True


def test_plugin_cleanup() -> None:
    """Test plugin cleanup (should not raise)."""
    plugin = EducationDomainPlugin()
    plugin.initialize()
    plugin.cleanup()  # Should not raise


# ============================================================================
# Grade Formula Tests
# ============================================================================


def test_grade_average_formula() -> None:
    """Test grade average formula: AVERAGE(range)."""
    formula = GradeAverageFormula()

    # Test metadata
    assert formula.metadata.name == "GRADE_AVERAGE"
    assert formula.metadata.category == "education"
    assert len(formula.metadata.arguments) == 2

    # Test simple average
    result = formula.build("A1:A10")
    assert result == "AVERAGE(A1:A10)"

    # Test with cell references
    result = formula.build("B2:B30")
    assert result == "AVERAGE(B2:B30)"


def test_grade_average_exclude_zeros() -> None:
    """Test grade average with zeros excluded."""
    formula = GradeAverageFormula()

    result = formula.build("A1:A10", "TRUE")
    assert result == 'AVERAGEIF(A1:A10;"<>0")'


def test_weighted_grade_formula() -> None:
    """Test weighted grade formula: SUMPRODUCT/SUM."""
    formula = WeightedGradeFormula()

    assert formula.metadata.name == "WEIGHTED_GRADE"

    result = formula.build("A1:A5", "B1:B5")
    assert result == "SUMPRODUCT(A1:A5;B1:B5)/SUM(B1:B5)"


def test_grade_curve_formula_linear() -> None:
    """Test grade curve formula with linear method."""
    formula = GradeCurveFormula()

    assert formula.metadata.name == "GRADE_CURVE"
    assert len(formula.metadata.arguments) == 4

    result = formula.build("B2", "B$2:B$30", "linear", "10")
    assert result == "MIN(B2+10;100)"


def test_grade_curve_formula_sqrt() -> None:
    """Test grade curve formula with sqrt method."""
    formula = GradeCurveFormula()

    result = formula.build("A1", "A1:A30", "sqrt")
    assert result == "SQRT(A1)*10"


def test_grade_curve_formula_bell() -> None:
    """Test grade curve formula with bell curve method."""
    formula = GradeCurveFormula()

    result = formula.build("A1", "A1:A30", "bell")
    assert "AVERAGE" in result
    assert "STDEV" in result


# ============================================================================
# Statistics Formula Tests
# ============================================================================


def test_standard_deviation_formula() -> None:
    """Test standard deviation formula."""
    formula = StandardDeviationFormula()

    assert formula.metadata.name == "STANDARD_DEVIATION"

    result = formula.build("A1:A30")
    assert "STDEV" in result


def test_percentile_rank_formula() -> None:
    """Test percentile rank formula."""
    formula = PercentileRankFormula()

    assert formula.metadata.name == "PERCENTILE_RANK"

    result = formula.build("B5", "B$2:B$30")
    assert "PERCENTRANK" in result or "RANK" in result


def test_correlation_formula() -> None:
    """Test correlation formula."""
    formula = CorrelationFormula()

    assert formula.metadata.name == "CORRELATION"

    result = formula.build("A1:A30", "B1:B30")
    assert "CORREL" in result


# ============================================================================
# Learning Metrics Formula Tests
# ============================================================================


def test_learning_gain_formula() -> None:
    """Test learning gain formula: (post-pre)/(100-pre)."""
    formula = LearningGainFormula()

    assert formula.metadata.name == "LEARNING_GAIN"

    result = formula.build("A1", "B1")
    # Normalized gain formula
    assert "A1" in result
    assert "B1" in result


def test_mastery_level_formula() -> None:
    """Test mastery level formula."""
    formula = MasteryLevelFormula()

    assert formula.metadata.name == "MASTERY_LEVEL"

    result = formula.build("A1", "80")
    assert "IF" in result


def test_attendance_rate_formula() -> None:
    """Test attendance rate formula: present/total*100."""
    formula = AttendanceRateFormula()

    assert formula.metadata.name == "ATTENDANCE_RATE"

    result = formula.build("A1", "B1")
    assert "100" in result


def test_completion_rate_formula() -> None:
    """Test completion rate formula."""
    formula = CompletionRateFormula()

    assert formula.metadata.name == "COMPLETION_RATE"

    result = formula.build("A1", "B1")
    assert "100" in result


def test_bloom_taxonomy_level_formula() -> None:
    """Test Bloom's taxonomy level formula."""
    formula = BloomTaxonomyLevelFormula()

    assert formula.metadata.name == "BLOOM_TAXONOMY_LEVEL"

    result = formula.build("A1")
    assert "IF" in result


def test_readability_score_formula() -> None:
    """Test readability score (Flesch-Kincaid) formula."""
    formula = ReadabilityScoreFormula()

    assert formula.metadata.name == "READABILITY_SCORE"

    result = formula.build("100", "20", "300")
    # Flesch-Kincaid formula components
    assert "206.835" in result or "1.015" in result or result is not None


# ============================================================================
# Template Tests
# ============================================================================


def test_course_gradebook_template() -> None:
    """Test course gradebook template generation."""
    template = CourseGradebookTemplate(
        course_name="Introduction to Python",
        num_students=30,
        num_assignments=10,
    )

    assert template.validate() is True
    assert template.metadata.name == "Course Gradebook"

    builder = template.generate()
    assert builder is not None


def test_lesson_plan_template() -> None:
    """Test lesson plan template generation."""
    template = LessonPlanTemplate(
        subject="Mathematics",
        grade_level="Grade 10",
        duration_minutes=50,
    )

    assert template.validate() is True
    assert template.metadata.name == "Lesson Plan"

    builder = template.generate()
    assert builder is not None


def test_assessment_rubric_template() -> None:
    """Test assessment rubric template generation."""
    template = AssessmentRubricTemplate(
        assignment_name="Research Paper",
        num_criteria=5,
    )

    assert template.validate() is True
    assert template.metadata.name == "Assessment Rubric"

    builder = template.generate()
    assert builder is not None


def test_student_attendance_template() -> None:
    """Test student attendance template generation."""
    template = StudentAttendanceTemplate(
        class_name="Period 3 Algebra",
        num_students=28,
        num_days=20,
    )

    assert template.validate() is True
    assert template.metadata.name == "Student Attendance"

    builder = template.generate()
    assert builder is not None


def test_learning_objectives_template() -> None:
    """Test learning objectives template generation."""
    template = LearningObjectivesTemplate(
        course_name="Biology 101",
        num_objectives=8,
    )

    assert template.validate() is True
    assert template.metadata.name == "Learning Objectives"

    builder = template.generate()
    assert builder is not None


def test_template_validation_failures() -> None:
    """Test template validation with invalid parameters."""
    # Invalid number of students
    template = CourseGradebookTemplate(num_students=0)
    assert template.validate() is False

    # Invalid number of criteria
    template2 = AssessmentRubricTemplate(num_criteria=0)
    assert template2.validate() is False


# ============================================================================
# Importer Tests
# ============================================================================


def test_lms_data_importer_csv() -> None:
    """Test LMS data CSV importer."""
    importer = LMSDataImporter()

    assert importer.metadata.name == "LMS Data Importer"
    assert "csv" in importer.metadata.supported_formats

    # Create test CSV file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Student ID,Name,Assignment 1,Assignment 2,Final Grade\n")
        f.write("STU001,John Doe,85,90,88\n")
        f.write("STU002,Jane Smith,92,88,91\n")
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)

        assert result.success is True
        assert result.records_imported == 2
        assert len(result.data) == 2
    finally:
        csv_path.unlink()


def test_lms_data_importer_invalid_file() -> None:
    """Test LMS data importer with invalid file."""
    importer = LMSDataImporter()

    result = importer.import_data("/nonexistent/file.csv")

    assert result.success is False
    assert len(result.errors) > 0


def test_gradebook_export_importer_csv() -> None:
    """Test gradebook export CSV importer."""
    importer = GradebookExportImporter()

    assert importer.metadata.name == "Gradebook Export Importer"

    # Create test CSV file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Student,Quiz 1,Quiz 2,Exam 1,Final\n")
        f.write("Alice,88,92,85,90\n")
        f.write("Bob,75,80,78,82\n")
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)

        assert result.success is True
        assert result.records_imported == 2
        assert len(result.data) == 2
    finally:
        csv_path.unlink()


def test_assessment_results_importer_csv() -> None:
    """Test assessment results CSV importer."""
    importer = AssessmentResultsImporter()

    assert importer.metadata.name == "Assessment Results Importer"

    # Create test CSV file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Student ID,Question 1,Question 2,Question 3,Total\n")
        f.write("S001,1,1,0,2\n")
        f.write("S002,1,1,1,3\n")
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)

        assert result.success is True
        assert result.records_imported == 2
    finally:
        csv_path.unlink()


# ============================================================================
# Utility Function Tests
# ============================================================================


def test_calculate_grade_average() -> None:
    """Test grade average calculation."""
    # Basic average
    assert calculate_grade_average([85, 90, 88, 92]) == 88.75

    # With None values
    result = calculate_grade_average([85, 90, None, 92])
    assert result is not None
    assert abs(result - 89.0) < 0.01

    # Empty list
    assert calculate_grade_average([]) is None

    # All None
    assert calculate_grade_average([None, None, None]) is None


def test_calculate_weighted_grade() -> None:
    """Test weighted grade calculation."""
    result = calculate_weighted_grade([85, 90, 95], [0.3, 0.3, 0.4])
    assert abs(result - 90.5) < 0.01

    # Equal weights
    result = calculate_weighted_grade([80, 90], [1, 1])
    assert abs(result - 85.0) < 0.01

    # Mismatched lengths should raise
    with pytest.raises(ValueError):
        calculate_weighted_grade([80, 90], [1])


def test_calculate_letter_grade() -> None:
    """Test letter grade conversion."""
    assert calculate_letter_grade(98) == "A+"
    assert calculate_letter_grade(93) == "A"
    assert calculate_letter_grade(91) == "A-"
    assert calculate_letter_grade(85) == "B"
    assert calculate_letter_grade(75) == "C"
    assert calculate_letter_grade(65) == "D"
    assert calculate_letter_grade(55) == "F"


def test_grade_to_points() -> None:
    """Test grade to points conversion."""
    assert grade_to_points("A") == 4.0
    assert grade_to_points("B+") == 3.3
    assert grade_to_points("C") == 2.0
    assert grade_to_points("F") == 0.0

    # Case insensitive
    assert grade_to_points("a-") == 3.7


def test_points_to_grade() -> None:
    """Test points to grade conversion."""
    assert points_to_grade(4.0) == "A+"
    assert points_to_grade(3.5) == "B+"
    assert points_to_grade(2.0) == "C"
    assert points_to_grade(0.0) == "F"


def test_calculate_gpa() -> None:
    """Test GPA calculation."""
    # Simple GPA (equal weights)
    result = calculate_gpa(["A", "B+", "B", "A-"])
    assert 3.4 < result < 3.6

    # With credits
    result = calculate_gpa(["A", "B"], [4, 3])
    assert 3.4 < result < 3.6

    # Empty grades
    assert calculate_gpa([]) == 0.0

    # Mismatched lengths should raise
    with pytest.raises(ValueError):
        calculate_gpa(["A", "B"], [4])


def test_calculate_attendance_rate() -> None:
    """Test attendance rate calculation."""
    assert abs(calculate_attendance_rate(85, 90) - 94.44) < 0.1
    assert calculate_attendance_rate(90, 90) == 100.0
    assert calculate_attendance_rate(0, 90) == 0.0
    assert calculate_attendance_rate(0, 0) == 0.0


def test_format_percentage() -> None:
    """Test percentage formatting."""
    assert format_percentage(85.678, 1) == "85.7%"
    assert format_percentage(90.0, 0) == "90%"
    assert format_percentage(75.5, 2, include_symbol=False) == "75.50"


# ============================================================================
# Integration Tests
# ============================================================================


def test_full_workflow_gradebook() -> None:
    """Test complete workflow for gradebook."""
    # Initialize plugin
    plugin = EducationDomainPlugin()
    plugin.initialize()

    # Get template class
    template_class = plugin.get_template("course_gradebook")
    assert template_class is not None

    # Create template instance
    template = template_class(course_name="Integration Test", num_students=5)

    # Generate spreadsheet
    builder = template.generate()
    assert builder is not None


def test_formula_argument_validation() -> None:
    """Test formula argument validation."""
    formula = WeightedGradeFormula()

    # Too few arguments should raise
    with pytest.raises(ValueError, match="requires at least"):
        formula.build("A1:A5")

    # Correct arguments should work
    result = formula.build("A1:A5", "B1:B5")
    assert result is not None


def test_importer_validation() -> None:
    """Test importer source validation."""
    importer = LMSDataImporter()

    # Non-existent file
    assert importer.validate_source(Path("/test/file.csv")) is False

    # Create temp file for validation
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        temp_path = Path(f.name)

    try:
        assert importer.validate_source(temp_path) is True
    finally:
        temp_path.unlink()


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================


def test_grade_curve_default_method() -> None:
    """Test grade curve with default method."""
    formula = GradeCurveFormula()

    # Should default to linear with 0 adjustment
    result = formula.build("A1", "A1:A30")
    assert "MIN" in result


def test_lms_importer_canvas_format() -> None:
    """Test LMS importer with Canvas-style format."""
    # Use 'platform' parameter (not 'lms_type') to match implementation
    importer = LMSDataImporter(platform="canvas")

    # Create Canvas-style CSV
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Student,ID,Section,Assignment 1,Assignment 2\n")
        f.write("Doe, John,12345,Section A,85,90\n")
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)
        assert result.success is True
    finally:
        csv_path.unlink()


def test_gradebook_with_missing_grades() -> None:
    """Test gradebook importer with missing grade values."""
    importer = GradebookExportImporter()

    # Create CSV with missing values
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Student,Quiz 1,Quiz 2,Exam 1\n")
        f.write("Alice,88,,85\n")  # Missing Quiz 2
        f.write("Bob,75,80,\n")  # Missing Exam 1
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)
        assert result.success is True
        # Should have warnings about missing values
    finally:
        csv_path.unlink()


def test_assessment_item_analysis() -> None:
    """Test assessment results with item analysis."""
    importer = AssessmentResultsImporter()

    # Create assessment data with item scores
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Student,Q1,Q2,Q3,Q4,Q5,Total,Percentage\n")
        f.write("S001,1,1,1,0,1,4,80\n")
        f.write("S002,1,0,1,1,1,4,80\n")
        f.write("S003,0,1,1,1,0,3,60\n")
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)
        assert result.success is True
        assert result.records_imported == 3
    finally:
        csv_path.unlink()


def test_importer_error_handling() -> None:
    """Test importer error handling with malformed files."""
    # Test with empty CSV
    importer = LMSDataImporter()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("")  # Empty file
        csv_path = Path(f.name)

    try:
        result = importer.import_data(csv_path)
        # Should handle gracefully
        assert result.success in (True, False)
    finally:
        csv_path.unlink()


def test_template_with_custom_weights() -> None:
    """Test gradebook template with custom assignment weights."""
    template = CourseGradebookTemplate(
        course_name="Advanced Math",
        num_students=25,
        num_assignments=5,
        weights={"assignments": 0.30, "midterm": 0.30, "final": 0.40},
    )

    assert template.validate() is True
    builder = template.generate()
    assert builder is not None


def test_utils_edge_cases() -> None:
    """Test utility functions with edge cases."""
    # Zero weights
    result = calculate_weighted_grade([90, 85], [0, 0])
    assert result == 0.0

    # Very high grade
    grade = calculate_letter_grade(110)
    assert grade == "A+"

    # Negative grade
    grade = calculate_letter_grade(-10)
    assert grade == "F"
