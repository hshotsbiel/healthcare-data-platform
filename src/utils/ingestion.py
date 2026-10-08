from datetime import datetime
from pathlib import Path
import csv
import shutil

from src.utils.ingestion_logger import log_ingestion


def ingest_csv(
    source_file: Path,
    bronze_dir: Path,
    entity: str,
    source: str,
    load_date: str,
    run_id: str,
):
    started_at = datetime.now()

    target_dir = bronze_dir / f"load_date={load_date}"
    target_file = target_dir / source_file.name

    load_type = "REPROCESS" if target_file.exists() else "INITIAL"

    try:
        target_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        with source_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            rows = list(csv.DictReader(file))

        rows_read = len(rows)

        shutil.copy2(
            source_file,
            target_file,
        )

        rows_written = rows_read

        finished_at = datetime.now()

        result = {
            "run_id": run_id,
            "entity": entity,
            "source": source,
            "load_date": load_date,
            "load_type": load_type,
            "status": "SUCCESS",
            "rows_read": rows_read,
            "rows_written": rows_written,
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "error_message": "",
        }

        log_ingestion(result)

        return result

    except Exception as error:
        finished_at = datetime.now()

        result = {
            "run_id": run_id,
            "entity": entity,
            "source": source,
            "load_date": load_date,
            "load_type": load_type,
            "status": "FAILED",
            "rows_read": 0,
            "rows_written": 0,
            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "error_message": str(error),
        }

        log_ingestion(result)

        raise