import logging
import pandas as pd
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def load_configuration() -> dict:
    """Load ETL configuration from YAML file."""
    config_path = PROJECT_ROOT / "config.yaml"
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise

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
    if file_path is None:
        config = load_configuration()
        file_path = PROJECT_ROOT / config['data']['raw_file']

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

if __name__ == "__main__":
    raw_data = extract()
    print(raw_data.head())
