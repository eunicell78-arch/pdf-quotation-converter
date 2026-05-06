#!/usr/bin/env python3
"""
Unit tests for the safe_get helper in converter.py.
Run with: python test_safe_get.py
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from converter import safe_get, normalize_lt_value, QuotationConverter


def test_safe_get():
    row = ['a', 'b', 'c']

    # Normal in-bounds access
    assert safe_get(row, 0) == 'a', "index 0 should return 'a'"
    assert safe_get(row, 2) == 'c', "index 2 should return 'c'"

    # Out-of-bounds access returns default
    assert safe_get(row, 3) == '', "index 3 (out of bounds) should return ''"
    assert safe_get(row, 10) == '', "index 10 (out of bounds) should return ''"

    # Negative indices are treated as out-of-bounds (safe, no wrap-around)
    assert safe_get(row, -1) == '', "negative index should return default, not row[-1]"
    assert safe_get(row, -2) == '', "negative index should return default"

    # Custom default
    assert safe_get(row, 5, default='N/A') == 'N/A', "custom default should be returned"

    # None row
    assert safe_get(None, 0) == '', "None row should return default"

    # None index
    assert safe_get(row, None) == '', "None index should return default"

    # Empty row
    assert safe_get([], 0) == '', "empty row should return default"

    # Single-column row
    assert safe_get(['only'], 0) == 'only', "single-col row index 0 should work"
    assert safe_get(['only'], 1) == '', "single-col row index 1 should return default"

    print("✅ All safe_get tests passed.")


def test_normalize_lt_value():
    assert normalize_lt_value(None) == '', "None should normalize to empty string"
    assert normalize_lt_value('') == '', "empty string should stay empty"
    assert normalize_lt_value('4-6') == '4-6wks', "range should get wks suffix"
    assert normalize_lt_value('4-6wk') == '4-6wks', "wk suffix should normalize to wks"
    assert normalize_lt_value('4-6wk.') == '4-6wks', "wk. suffix should normalize to wks"
    assert normalize_lt_value('4-6 wks') == '4-6wks', "spaced wks should normalize to compact wks"
    assert normalize_lt_value('4-6week') == '4-6wks', "week suffix should normalize to wks"
    assert normalize_lt_value('4-6 weeks') == '4-6wks', "weeks suffix should normalize to wks"
    assert normalize_lt_value('4-6WKS') == '4-6wks', "uppercase WKS should normalize to lowercase wks"
    assert normalize_lt_value('10') == '10wks', "single numeric value should get wks suffix"
    assert normalize_lt_value('wk') == 'wks', "unit-only wk should normalize to wks"
    assert normalize_lt_value('WK') == 'wks', "uppercase WK should normalize to wks"
    assert normalize_lt_value('week') == 'wks', "unit-only week should normalize to wks"
    assert normalize_lt_value('WEEKS') == 'wks', "uppercase WEEKS should normalize to wks"
    assert normalize_lt_value('weeks') == 'wks', "unit-only weeks should normalize to wks"
    print("✅ All normalize_lt_value tests passed.")


def _converter():
    """Return a QuotationConverter instance without requiring a real PDF."""
    return QuotationConverter.__new__(QuotationConverter)


def test_parse_product_field():
    conv = _converter()

    # Standard case: colon with no surrounding spaces
    product, rc, cl, desc = conv.parse_product_field(
        "TYPE1 AC Charging Cable, Gen3\n"
        "- Rated Current: 32A\n"
        "- Cable Length: 5M\n"
        "- No thermal sensor\n"
        "- Production Site : China"
    )
    assert product == "TYPE1 AC Charging Cable, Gen3", f"product: {product!r}"
    assert rc == "32A", f"rated_current: {rc!r}"
    assert cl == "5M", f"cable_length: {cl!r}"
    assert desc == "No thermal sensor\nProduction Site : China", f"description: {desc!r}"

    # Space before colon: 'Rated Current : 32A'
    product, rc, cl, desc = conv.parse_product_field(
        "TYPE1 AC Charging Cable, Gen3\n"
        "- Rated Current : 32A\n"
        "- Cable Length : 5M\n"
        "- No thermal sensor\n"
        "- Production Site : China"
    )
    assert product == "TYPE1 AC Charging Cable, Gen3", f"product: {product!r}"
    assert rc == "32A", f"rated_current with space: {rc!r}"
    assert cl == "5M", f"cable_length with space: {cl!r}"
    assert desc == "No thermal sensor\nProduction Site : China", f"description: {desc!r}"

    # No Rated Current / Cable Length → description stays empty, product is first line
    product, rc, cl, desc = conv.parse_product_field("Simple Product Name")
    assert product == "Simple Product Name", f"product: {product!r}"
    assert rc == "", f"rated_current: {rc!r}"
    assert cl == "", f"cable_length: {cl!r}"
    assert desc == "", f"description: {desc!r}"

    print("✅ All parse_product_field tests passed.")


def test_header_parsing():
    conv = _converter()

    # Helper: build a minimal fake page object
    class FakePage:
        def __init__(self, text):
            self._text = text
        def extract_text(self):
            return self._text

    # To and From on separate lines
    page = FakePage("To: EV Mode\nFrom: Sherry Liu\nDate: Dec. 22, 2025\nRef: Q-001")
    header = conv.extract_header_info(page)
    assert header.get('customer') == 'EV Mode', f"customer: {header.get('customer')!r}"
    assert header.get('planner') == 'Sherry Liu', f"planner: {header.get('planner')!r}"

    # To and From on the same line
    page = FakePage("To: EV Mode From: Sherry Liu\nDate: Dec. 22, 2025")
    header = conv.extract_header_info(page)
    assert header.get('customer') == 'EV Mode', f"customer (same-line): {header.get('customer')!r}"
    assert header.get('planner') == 'Sherry Liu', f"planner (same-line): {header.get('planner')!r}"

    print("✅ All header parsing tests passed.")


if __name__ == '__main__':
    test_safe_get()
    test_normalize_lt_value()
    test_parse_product_field()
    test_header_parsing()
