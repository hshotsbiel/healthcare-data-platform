from datetime import datetime
from pathlib import Path
import uuid

from src.utils.ingestion import ingest_csv


BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_FILE = BASE_DIR / "data" / "sample" / "patients.csv"
BRONZE_DIR = BASE_DIR / "data" / "bronze" / "patients"


if __name__ == "__main__":
    load_date = datetime.now().date().isoformat()
    run_id = str(uuid.uuid4())

    result = ingest_csv(
        source_file=SOURCE_FILE,
        bronze_dir=BRONZE_DIR,
        entity="patients",
        source="synthetic_csv",
        load_date=load_date,
        run_id=run_id,
    )

    print(result)