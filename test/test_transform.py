"""
Tests for etl/transform.py

These tests verify that:
- transform() returns a dict with the correct keys
- Column names are converted to snake_case
- Dates are converted to datetime
- Postal codes are cleaned (no nulls, string type)
- row_id is dropped
- Surrogate keys are correct
- Fact table row count matches input
- Dimension tables have no duplicates
- Empty DataFrames raise ValueError
"""
import pytest
import pandas as pd
from etl.transform import (
    transform,
    build_dim_customer,
    build_dim_product,
    build_dim_location,
    build_fact_sales,
)


# ===========================================================================
# TRANSFORM() — Main function tests
# ===========================================================================

class TestTransformOutput:
    """Tests for the overall transform() function output."""

    def test_returns_dict(self, sample_raw_data):
        """transform() should return a dictionary."""
        result = transform(sample_raw_data)
        assert isinstance(result, dict)

    def test_expected_keys(self, sample_raw_data):
        """The dict should contain exactly these 4 keys."""
        result = transform(sample_raw_data)
        expected_keys = {"fact_sales", "dim_customer", "dim_product", "dim_location"}
        assert set(result.keys()) == expected_keys

    def test_all_values_are_dataframes(self, sample_raw_data):
        """Every value in the dict should be a DataFrame."""
        result = transform(sample_raw_data)
        for name, df in result.items():
            assert isinstance(df, pd.DataFrame), f"{name} is not a DataFrame"

    def test_empty_dataframe_raises(self, sample_empty_data):
        """Passing an empty DataFrame should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            transform(sample_empty_data)

    def test_does_not_modify_original(self, sample_raw_data):
        """transform() should work on a copy, not modify the input."""
        original_columns = list(sample_raw_data.columns)
        original_len = len(sample_raw_data)
        transform(sample_raw_data)
        assert list(sample_raw_data.columns) == original_columns
        assert len(sample_raw_data) == original_len


# ===========================================================================
# DATA CLEANING — Column names, dates, postal codes, dropped columns
# ===========================================================================

class TestDataCleaning:
    """Tests for the cleaning transformations applied before building dims."""

    def test_columns_are_snake_case(self, sample_raw_data):
        """All column names should be lowercase with underscores, no spaces."""
        result = transform(sample_raw_data)
        for name, df in result.items():
            for col in df.columns:
                assert col == col.lower(), f"Column '{col}' in {name} is not lowercase"
                assert " " not in col, f"Column '{col}' in {name} has spaces"

    def test_order_date_is_datetime(self, sample_raw_data):
        """order_date should be datetime64 after transformation."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        assert pd.api.types.is_datetime64_any_dtype(fact["order_date"])

    def test_ship_date_is_datetime(self, sample_raw_data):
        """ship_date should be datetime64 after transformation."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        assert pd.api.types.is_datetime64_any_dtype(fact["ship_date"])

    def test_postal_code_is_string(self, sample_raw_data):
        """postal_code should be converted to string (object dtype)."""
        result = transform(sample_raw_data)
        dim_loc = result["dim_location"]
        assert dim_loc["postal_code"].dtype == "object"

    def test_postal_code_no_nulls(self, sample_raw_data):
        """Null postal codes should be filled (no NaN values remaining)."""
        result = transform(sample_raw_data)
        dim_loc = result["dim_location"]
        assert dim_loc["postal_code"].isnull().sum() == 0

    def test_postal_code_null_filled_correctly(self, sample_raw_data):
        """The null postal code (Burlington, VT) should be filled with '5401'."""
        result = transform(sample_raw_data)
        dim_loc = result["dim_location"]
        assert "5401" in dim_loc["postal_code"].values

    def test_row_id_not_in_any_table(self, sample_raw_data):
        """row_id should be dropped and not appear in any output table."""
        result = transform(sample_raw_data)
        for name, df in result.items():
            assert "row_id" not in df.columns, f"row_id found in {name}"


# ===========================================================================
# DIMENSION TABLES — Uniqueness, surrogate keys, columns
# ===========================================================================

class TestDimCustomer:
    """Tests for the dim_customer dimension table."""

    def test_no_duplicate_customers(self, sample_raw_data):
        """Each customer should appear exactly once."""
        result = transform(sample_raw_data)
        dim = result["dim_customer"]
        assert dim["customer_id"].is_unique

    def test_has_surrogate_key(self, sample_raw_data):
        """dim_customer should have a customer_sk column."""
        result = transform(sample_raw_data)
        dim = result["dim_customer"]
        assert "customer_sk" in dim.columns

    def test_surrogate_key_starts_at_1(self, sample_raw_data):
        """Surrogate keys should start at 1, not 0."""
        result = transform(sample_raw_data)
        dim = result["dim_customer"]
        assert dim["customer_sk"].min() == 1

    def test_surrogate_key_is_sequential(self, sample_raw_data):
        """Surrogate keys should be sequential: 1, 2, 3, ..."""
        result = transform(sample_raw_data)
        dim = result["dim_customer"]
        expected = list(range(1, len(dim) + 1))
        assert list(dim["customer_sk"]) == expected

    def test_expected_columns(self, sample_raw_data):
        """dim_customer should have exactly these columns."""
        result = transform(sample_raw_data)
        dim = result["dim_customer"]
        expected = {"customer_sk", "customer_id", "customer_name", "segment"}
        assert set(dim.columns) == expected

    def test_correct_count(self, sample_raw_data):
        """Sample data has 2 unique customers (CG-001 and DV-002)."""
        result = transform(sample_raw_data)
        dim = result["dim_customer"]
        assert len(dim) == 2


class TestDimProduct:
    """Tests for the dim_product dimension table."""

    def test_no_duplicate_products(self, sample_raw_data):
        """Each product should appear exactly once."""
        result = transform(sample_raw_data)
        dim = result["dim_product"]
        assert dim["product_id"].is_unique

    def test_has_surrogate_key(self, sample_raw_data):
        """dim_product should have a product_sk column."""
        result = transform(sample_raw_data)
        dim = result["dim_product"]
        assert "product_sk" in dim.columns

    def test_surrogate_key_starts_at_1(self, sample_raw_data):
        result = transform(sample_raw_data)
        dim = result["dim_product"]
        assert dim["product_sk"].min() == 1

    def test_expected_columns(self, sample_raw_data):
        """dim_product should have exactly these columns."""
        result = transform(sample_raw_data)
        dim = result["dim_product"]
        expected = {"product_sk", "product_id", "product_name", "category", "sub_category"}
        assert set(dim.columns) == expected

    def test_correct_count(self, sample_raw_data):
        """Sample data has 3 unique products."""
        result = transform(sample_raw_data)
        dim = result["dim_product"]
        assert len(dim) == 3


class TestDimLocation:
    """Tests for the dim_location dimension table."""

    def test_no_duplicate_locations(self, sample_raw_data):
        """Each location (city+state+postal_code) should appear once."""
        result = transform(sample_raw_data)
        dim = result["dim_location"]
        location_cols = ["city", "state", "postal_code"]
        assert not dim.duplicated(subset=location_cols).any()

    def test_has_surrogate_key(self, sample_raw_data):
        result = transform(sample_raw_data)
        dim = result["dim_location"]
        assert "location_sk" in dim.columns

    def test_surrogate_key_starts_at_1(self, sample_raw_data):
        result = transform(sample_raw_data)
        dim = result["dim_location"]
        assert dim["location_sk"].min() == 1

    def test_expected_columns(self, sample_raw_data):
        """dim_location should have exactly these columns."""
        result = transform(sample_raw_data)
        dim = result["dim_location"]
        expected = {"location_sk", "region", "country", "city", "state", "postal_code"}
        assert set(dim.columns) == expected


# ===========================================================================
# FACT TABLE — Row count, surrogate keys, no natural keys
# ===========================================================================

class TestFactSales:
    """Tests for the fact_sales fact table."""

    def test_row_count_matches_input(self, sample_raw_data):
        """Fact table should have the same number of rows as the input."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        assert len(fact) == len(sample_raw_data)

    def test_has_surrogate_keys(self, sample_raw_data):
        """Fact table should contain all three surrogate key columns."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        assert "customer_sk" in fact.columns
        assert "product_sk" in fact.columns
        assert "location_sk" in fact.columns

    def test_no_natural_keys(self, sample_raw_data):
        """Fact table should NOT contain dimension natural key columns."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        natural_keys = [
            "customer_id", "customer_name", "segment",
            "product_id", "product_name", "category", "sub_category",
            "city", "state", "postal_code", "region", "country",
        ]
        for col in natural_keys:
            assert col not in fact.columns, f"Natural key '{col}' should not be in fact_sales"

    def test_expected_columns(self, sample_raw_data):
        """Fact table should have exactly these columns."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        expected = {
            "order_id", "order_date", "ship_date", "ship_mode",
            "sales", "customer_sk", "product_sk", "location_sk",
        }
        assert set(fact.columns) == expected

    def test_sales_values_preserved(self, sample_raw_data):
        """Sales values should not be altered during transformation."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]
        original_total = sample_raw_data["Sales"].sum()
        transformed_total = fact["sales"].sum()
        assert abs(original_total - transformed_total) < 0.01

    def test_surrogate_keys_reference_dimensions(self, sample_raw_data):
        """Every surrogate key in fact_sales should exist in the dimension."""
        result = transform(sample_raw_data)
        fact = result["fact_sales"]

        customer_sks = set(result["dim_customer"]["customer_sk"])
        product_sks = set(result["dim_product"]["product_sk"])
        location_sks = set(result["dim_location"]["location_sk"])

        assert set(fact["customer_sk"]).issubset(customer_sks)
        assert set(fact["product_sk"]).issubset(product_sks)
        assert set(fact["location_sk"]).issubset(location_sks)
