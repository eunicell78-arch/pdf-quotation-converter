#!/usr/bin/env python3
"""
Unit tests for the safe_get helper in converter.py.
Run with: python test_safe_get.py
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from converter import safe_get


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


if __name__ == '__main__':
    test_safe_get()
