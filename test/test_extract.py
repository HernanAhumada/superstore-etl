"""
Tests for etl/extract.py

These tests verify that:
- extract() returns a DataFrame when given a valid file
- extract() raises FileNotFoundError for missing files
- extract() raises ValueError for empty files
- The returned DataFrame has the expected shape and columns
"""
import pytest
import pandas as pd
from pathlib import Path
from etl.extract import extract


# ---------------------------------------------------------------------------
# Test: extract raises FileNotFoundError for a nonexistent file
# ---------------------------------------------------------------------------
def test_extract_file_not_found():
    """Passing a path that doesn't exist should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        extract("this/file/does/not/exist.csv")


# ---------------------------------------------------------------------------
# Test: extract raises ValueError for an empty CSV
# ---------------------------------------------------------------------------
def test_extract_empty_file(tmp_path):
    """
    An empty CSV (headers only, no rows) should raise ValueError.

    tmp_path is a built-in pytest fixture that creates a temporary
    directory unique to this test. It's automatically cleaned up.
    """
    # Create a CSV with headers but no data rows
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("Row ID,Order ID,Order Date\n")

    with pytest.raises(ValueError, match="empty"):
        extract(str(empty_csv))


# ---------------------------------------------------------------------------
# Test: extract returns a DataFrame with the correct structure
# ---------------------------------------------------------------------------
def test_extract_returns_dataframe(tmp_path):
    """extract() should return a pandas DataFrame."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "Row ID,Order ID,Sales\n"
        "1,CA-2017-001,100.0\n"
        "2,CA-2017-002,200.0\n"
    )
    result = extract(str(csv_file))
    assert isinstance(result, pd.DataFrame)


def test_extract_row_count(tmp_path):
    """The DataFrame should have the same number of rows as the CSV."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "Row ID,Order ID,Sales\n"
        "1,CA-2017-001,100.0\n"
        "2,CA-2017-002,200.0\n"
        "3,CA-2017-003,300.0\n"
    )
    result = extract(str(csv_file))
    assert len(result) == 3


def test_extract_columns(tmp_path):
    """The DataFrame should contain the columns from the CSV header."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "Row ID,Order ID,Sales\n"
        "1,CA-2017-001,100.0\n"
    )
    result = extract(str(csv_file))
    assert list(result.columns) == ["Row ID", "Order ID", "Sales"]
