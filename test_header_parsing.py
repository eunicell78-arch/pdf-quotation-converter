#!/usr/bin/env python3
"""
Unit tests for extract_header_info() in converter.py.
Run with: python test_header_parsing.py
"""

import sys
import os
import types

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from converter import QuotationConverter as PDFConverter


def _make_page(text: str):
    """Return a minimal mock page object whose extract_text() returns *text*."""
    page = types.SimpleNamespace()
    page.extract_text = lambda: text
    return page


def _parse(text: str) -> dict:
    """Run extract_header_info on *text* and return the resulting dict."""
    converter = PDFConverter.__new__(PDFConverter)
    return converter.extract_header_info(_make_page(text))


def test_combined_line():
    """Acceptance criterion: To and From on the same line are split correctly."""
    header = _parse("To: EVSIS Co., Ltd From: Sherry Liu")
    assert header.get('customer') == "EVSIS Co., Ltd", (
        f"customer should be 'EVSIS Co., Ltd', got {header.get('customer')!r}"
    )
    assert header.get('planner') == "Sherry Liu", (
        f"planner should be 'Sherry Liu', got {header.get('planner')!r}"
    )


def test_separate_lines():
    """Existing behavior: To and From on separate lines still parse correctly."""
    text = "To: EVSIS Co., Ltd\nFrom: Sherry Liu"
    header = _parse(text)
    assert header.get('customer') == "EVSIS Co., Ltd", (
        f"customer should be 'EVSIS Co., Ltd', got {header.get('customer')!r}"
    )
    assert header.get('planner') == "Sherry Liu", (
        f"planner should be 'Sherry Liu', got {header.get('planner')!r}"
    )


def test_from_with_space_before_colon():
    """'From :' (space before colon) is treated the same as 'From:'."""
    text = "To: EVSIS Co., Ltd From : Sherry Liu"
    header = _parse(text)
    assert header.get('customer') == "EVSIS Co., Ltd", (
        f"customer should be 'EVSIS Co., Ltd', got {header.get('customer')!r}"
    )
    assert header.get('planner') == "Sherry Liu", (
        f"planner should be 'Sherry Liu', got {header.get('planner')!r}"
    )


def test_from_only_line():
    """A line that starts with From: (no preceding To:) sets planner."""
    header = _parse("From: Jane Doe")
    assert header.get('planner') == "Jane Doe", (
        f"planner should be 'Jane Doe', got {header.get('planner')!r}"
    )
    assert header.get('customer') is None, "customer should not be set"


def test_to_only_line():
    """A line with only To: (no From:) sets only customer."""
    header = _parse("To: Acme Corp")
    assert header.get('customer') == "Acme Corp", (
        f"customer should be 'Acme Corp', got {header.get('customer')!r}"
    )
    assert header.get('planner') is None, "planner should not be set"


def test_extra_whitespace():
    """Extra spaces around names are stripped."""
    header = _parse("To:   EVSIS Co., Ltd   From:   Sherry Liu   ")
    assert header.get('customer') == "EVSIS Co., Ltd", (
        f"customer not stripped correctly: {header.get('customer')!r}"
    )
    assert header.get('planner') == "Sherry Liu", (
        f"planner not stripped correctly: {header.get('planner')!r}"
    )


def test_multiline_block():
    """Full synthetic header block with Date and Ref still parses all fields."""
    text = (
        "To: EVSIS Co., Ltd From: Sherry Liu\n"
        "Date: 2024-01-15\n"
        "Ref: Q-2024-001\n"
    )
    header = _parse(text)
    assert header.get('customer') == "EVSIS Co., Ltd"
    assert header.get('planner') == "Sherry Liu"
    # Date and Ref parsing is unchanged
    assert header.get('date') == "2024-01-15", (
        f"date should be '2024-01-15', got {header.get('date')!r}"
    )
    assert header.get('ref') == "Q-2024-001", (
        f"ref should be 'Q-2024-001', got {header.get('ref')!r}"
    )


if __name__ == '__main__':
    test_combined_line()
    print("✅ test_combined_line passed")
    test_separate_lines()
    print("✅ test_separate_lines passed")
    test_from_with_space_before_colon()
    print("✅ test_from_with_space_before_colon passed")
    test_from_only_line()
    print("✅ test_from_only_line passed")
    test_to_only_line()
    print("✅ test_to_only_line passed")
    test_extra_whitespace()
    print("✅ test_extra_whitespace passed")
    test_multiline_block()
    print("✅ test_multiline_block passed")
    print("\n✅ All header parsing tests passed.")
