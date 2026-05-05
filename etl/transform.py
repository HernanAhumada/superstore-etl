import pandas as pd
import logging

logger = logging.getLogger(__name__)

def build_dim_customer(transformed_df: pd.DataFrame) -> pd.DataFrame:
    """Extract unique customers and add a customer key
    """
    dim_customer = (transformed_df[["customer_id", "customer_name", "segment"]]
                        .drop_duplicates()
                        .reset_index(drop=True))
    logger.info(f"dim_customer: {len(dim_customer)} unique customers")
    dim_customer.insert(0, "customer_sk", dim_customer.index + 1)
    return dim_customer

def build_dim_product(transformed_df: pd.DataFrame) -> pd.DataFrame:
    """Extract unique products and add a product key
    """
    dim_product = (transformed_df[["product_id", "product_name", "category", "sub_category"]]
                    .drop_duplicates()
                    .reset_index(drop=True))
    logger.info(f"dim_product: {len(dim_product)} unique products")
    dim_product.insert(0, "product_sk", dim_product.index + 1)
    return dim_product

def build_dim_location(transformed_df:pd.DataFrame) -> pd.DataFrame:
    """Extract unique location data and add a location key
    """
    dim_location = (transformed_df[["region", "country", "city", "state", "postal_code"]]
                     .drop_duplicates()
                     .reset_index(drop=True))
    logger.info(f"dim_location: {len(dim_location)} unique locations")
    dim_location.insert(0, "location_sk", dim_location.index + 1)
    return dim_location

def build_fact_sales(transformed_df:pd.DataFrame, dim_customer:pd.DataFrame, dim_product:pd.DataFrame, dim_location:pd.DataFrame) -> pd.DataFrame:
    """Build the sales fact table by merging all dimension tables
    """
    fact_sales = (transformed_df.merge(dim_customer, on=["customer_id", "customer_name", "segment"])
                    .merge(dim_product, on=["product_id", "product_name", "category", "sub_category"])
                    .merge(dim_location, on=["region", "country", "city", "state", "postal_code"])
                )
    fact_sales = fact_sales.drop(columns=["customer_id",
                                          "customer_name",
                                          "segment",
                                          "country",
                                          "city",
                                          "state",
                                          "postal_code",
                                          "region",
                                          "product_id",
                                          "product_name",
                                          "category",
                                          "sub_category"])
    logger.info(f"fact_sales: {len(fact_sales)} sales records")
    return fact_sales

def transform(df: pd.DataFrame) -> dict:
    """Transform raw data into clean, analytics-ready format.
    Args:
        df: Raw DataFrame from extract.py
    Returns:
        dictionary of dataframes for fact and dimension tables with keys: 
        'fact_sales', 'dim_customer', 'dim_product', 'dim_location'
    """
    logger.info("Transforming data")

    transformed_df = df.copy()

    transformed_df.columns = transformed_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-','_')
    transformed_df["order_date"] = pd.to_datetime(transformed_df["order_date"], format="%d/%m/%Y")
    transformed_df["ship_date"] = pd.to_datetime(transformed_df["ship_date"], format="%d/%m/%Y")
    transformed_df["postal_code"] = transformed_df["postal_code"].fillna(5401).astype(int).astype(str)
    transformed_df = transformed_df.drop(columns=["row_id"])

    if transformed_df.empty:
        logger.error("DataFrame is empty after transformation.")
        raise ValueError("DataFrame is empty after transformation.")
    
    expected_columns = {"order_id", "order_date", "ship_date", "ship_mode",
                        "customer_id", "customer_name", "segment", "country", "city",
                        "state", "postal_code", "region", "product_id",
                        "category", "sub_category", "product_name", "sales"}
    missing_columns = expected_columns - set(transformed_df.columns)

    if missing_columns:
        logger.error(f"Missing expected columns after transformation: {missing_columns}")
        raise ValueError(f"Missing expected columns after transformation: {missing_columns}")
    logger.info(f"Transformed data shape: {transformed_df.shape}")

    dim_customer = build_dim_customer(transformed_df)
    dim_product = build_dim_product(transformed_df)
    dim_location = build_dim_location(transformed_df)
    fact_sales = build_fact_sales(transformed_df, dim_customer, dim_product, dim_location)

    return {"fact_sales": fact_sales, 
            "dim_customer": dim_customer, 
            "dim_product": dim_product, 
            "dim_location": dim_location }