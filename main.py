import logging
import time
from sqlalchemy import create_engine
from etl.config import load_configuration, PROJECT_ROOT
from etl.extract import extract
from etl.transform import transform
from etl.load import load

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # 1. Setup logging
    # 2. Load config, create engine
    # 3. Extract → Transform → Load
    # 4. Log elapsed time
    start_time = time.time()
    logger.info(f"Starting ETL process {start_time}")

    config = load_configuration()
    file_path = PROJECT_ROOT / config['data']['raw_file']
    engine_string = config['database']['connection_string']
    engine = create_engine(engine_string)

    raw_data = extract(file_path)
    logger.info("extract process completed.")

    transformed_data = transform(raw_data)
    logger.info("transform process completed.")

    load(transformed_data, engine)
    logger.info("load process completed successfully.")
    
    elapsed_time = time.time() - start_time
    logger.info(f"ETL process completed successfully in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
