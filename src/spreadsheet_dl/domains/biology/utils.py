"""
Utility functions for biology domain.

Implements:
    TASK-C006: Biology domain utility functions
"""

from __future__ import annotations


def calculate_gc_content(sequence: str) -> float:
    """
    Calculate GC content of a DNA sequence.

    Args:
        sequence: DNA sequence string

    Returns:
        GC content as percentage (0-100)

    Example:
        >>> calculate_gc_content("ATGCATGC")
        50.0
    """
    if not sequence:
        return 0.0

    sequence = sequence.upper()
    g_count = sequence.count("G")
    c_count = sequence.count("C")
    total = len(sequence)

    if total == 0:
        return 0.0

    return ((g_count + c_count) / total) * 100


def calculate_melting_temp(sequence: str) -> float:
    """
    Calculate DNA melting temperature using basic formula.

    Args:
        sequence: DNA sequence string

    Returns:
        Melting temperature in Celsius

    Example:
        >>> calculate_melting_temp("ATGCATGC")
        24.0
    """
    if not sequence:
        return 0.0

    sequence = sequence.upper()
    length = len(sequence)

    # For short sequences (< 14 bp): Tm = 4(G+C) + 2(A+T)
    if length < 14:
        g_count = sequence.count("G")
        c_count = sequence.count("C")
        a_count = sequence.count("A")
        t_count = sequence.count("T")
        return 4.0 * (g_count + c_count) + 2.0 * (a_count + t_count)

    # For longer sequences: use GC content method
    # Tm = 64.9 + 41 * (yG + zC - 16.4) / (wA + xT + yG + zC)
    gc_content = calculate_gc_content(sequence)
    return 64.9 + 41.0 * (gc_content / 100.0 - 0.41)


def normalize_sequence(sequence: str) -> str:
    """
    Normalize DNA/RNA sequence string.

    Args:
        sequence: Raw sequence string

    Returns:
        Normalized sequence (uppercase, whitespace removed)

    Example:
        >>> normalize_sequence("atg c")
        'ATGC'
    """
    return "".join(sequence.split()).upper()


def is_valid_dna(sequence: str) -> bool:
    """
    Check if string is a valid DNA sequence.

    Args:
        sequence: Sequence string to validate

    Returns:
        True if valid DNA sequence

    Example:
        >>> is_valid_dna("ATGC")
        True
        >>> is_valid_dna("ATGCX")
        False
    """
    valid_bases = set("ATGCN")
    return set(normalize_sequence(sequence)).issubset(valid_bases)


def is_valid_rna(sequence: str) -> bool:
    """
    Check if string is a valid RNA sequence.

    Args:
        sequence: Sequence string to validate

    Returns:
        True if valid RNA sequence

    Example:
        >>> is_valid_rna("AUGC")
        True
        >>> is_valid_rna("ATGC")
        False
    """
    valid_bases = set("AUGCN")
    return set(normalize_sequence(sequence)).issubset(valid_bases)


def complement_dna(sequence: str) -> str:
    """
    Get complement of DNA sequence.

    Args:
        sequence: DNA sequence string

    Returns:
        Complement sequence

    Example:
        >>> complement_dna("ATGC")
        'TACG'
    """
    complement_map = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
    sequence = normalize_sequence(sequence)
    return "".join(complement_map.get(base, "N") for base in sequence)


def reverse_complement(sequence: str) -> str:
    """
    Get reverse complement of DNA sequence.

    Args:
        sequence: DNA sequence string

    Returns:
        Reverse complement sequence

    Example:
        >>> reverse_complement("ATGC")
        'GCAT'
    """
    return complement_dna(sequence)[::-1]


__all__ = [
    "calculate_gc_content",
    "calculate_melting_temp",
    "normalize_sequence",
    "is_valid_dna",
    "is_valid_rna",
    "complement_dna",
    "reverse_complement",
]
