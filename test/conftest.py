"""
Shared fixtures for all test files.

Fixtures defined here are automatically available to every test
without importing them — pytest discovers conftest.py automatically.
"""
import pytest
import pandas as pd


@pytest.fixture
def sample_raw_data():
    """
    Fake raw data that matches the structure of train.csv.

    This has 4 rows with:
    - 2 customers
    - 3 products
    - 2 locations (Henderson and Los Angeles)
    - 1 null Postal Code (to test the fillna logic)
    """
    return pd.DataFrame({
        "Row ID": [1, 2, 3, 4],
        "Order ID": ["CA-2017-001", "CA-2017-001", "CA-2017-002", "CA-2017-003"],
        "Order Date": ["08/11/2017", "08/11/2017", "12/06/2017", "15/03/2018"],
        "Ship Date": ["11/11/2017", "11/11/2017", "16/06/2017", "20/03/2018"],
        "Ship Mode": ["Second Class", "Second Class", "Standard Class", "First Class"],
        "Customer ID": ["CG-001", "CG-001", "DV-002", "DV-002"],
        "Customer Name": ["Claire Gute", "Claire Gute", "Darrin Van Huff", "Darrin Van Huff"],
        "Segment": ["Consumer", "Consumer", "Corporate", "Corporate"],
        "Country": ["United States", "United States", "United States", "United States"],
        "City": ["Henderson", "Henderson", "Los Angeles", "Los Angeles"],
        "State": ["Kentucky", "Kentucky", "California", "California"],
        "Postal Code": [42420.0, 42420.0, 90036.0, None],  # one null to test fillna
        "Region": ["South", "South", "West", "West"],
        "Product ID": ["FUR-BO-001", "FUR-CH-002", "OFF-LA-003", "FUR-BO-001"],
        "Category": ["Furniture", "Furniture", "Office Supplies", "Furniture"],
        "Sub-Category": ["Bookcases", "Chairs", "Labels", "Bookcases"],
        "Product Name": ["Bookcase A", "Chair B", "Labels C", "Bookcase A"],
        "Sales": [261.96, 731.94, 14.62, 100.00],
    })


@pytest.fixture
def sample_empty_data():
    """An empty DataFrame with the correct columns (to test empty validation)."""
    return pd.DataFrame(columns=[
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "Country", "City",
        "State", "Postal Code", "Region", "Product ID", "Category",
        "Sub-Category", "Product Name", "Sales",
    ])
