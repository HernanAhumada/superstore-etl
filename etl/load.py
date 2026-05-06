import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

def load(tables: dict, engine) -> None:
    """
    Load transformed DataFrames into PostgreSQL.
    Args:
        tables: Dict of table_name -> DataFrame from transform step.
        engine: SQLAlchemy engine connected to the target database.
    Raises:
        Exception: If any table fails to load.
    """
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE fact_sales"))
        conn.execute(text("TRUNCATE TABLE dim_customer CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_product CASCADE"))
        conn.execute(text("TRUNCATE TABLE dim_location CASCADE"))
        conn.commit()
    logger.info("Truncated all tables")

    load_order = ["dim_product", "dim_customer", "dim_location", "fact_sales"]

    for table_name in load_order:
        df = tables[table_name]
        try:
            df.to_sql(table_name, engine, if_exists='append', index=False)
            logger.info(f"Loaded {len(df)} rows into {table_name}")
        except Exception as e:
            logger.error(f"Failed to load table {table_name}: {e}")
            raise