import logging
import pandas as pd

logger = logging.getLogger(__name__)

def extract(file_path: str | None = None) -> pd.DataFrame:
    """
    Extract raw data from CSV.
    Args:
        file_path: Optional override. If None, reads from config.yaml.
    Returns:
        pd.DataFrame with the raw Superstore data.
    Raises:
        ValueError: If the extracted data is empty.
        FileNotFoundError: If the CSV file doesn't exist.
    """

    logger.info(f"Extracting data from {file_path}")

    try:
        raw_data = pd.read_csv(file_path)
        if raw_data.empty:
            raise ValueError(f"Extracted data is empty. {file_path}")
        logger.info(f"Extracted {len(raw_data)} rows, {len(raw_data.columns)} columns")
        return raw_data
    except FileNotFoundError:
        logger.error(f"File not found at {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error extracting data: {e}")
        raise
