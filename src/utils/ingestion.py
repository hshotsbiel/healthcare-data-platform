from datetime import datetime
from pathlib import Path
import csv

from src.utils.ingestion_logger import log_ingestion
from src.utils.watermark import (
    get_watermark,
    save_watermark,
)


def ingest_csv(
    source_file: Path,
    bronze_dir: Path,
    entity: str,
    source: str,
    load_date: str,
    run_id: str,
    watermark: str | None = None,
    watermark_column: str = "created_at",
):
    started_at = datetime.now()

    target_dir = bronze_dir / f"load_date={load_date}"
    target_file = target_dir / source_file.name

    current_watermark = get_watermark(entity)

    if watermark is None and current_watermark is not None:
        watermark = current_watermark["watermark_value"]

    load_type = (
        "INCREMENTAL"
        if watermark is not None
        else "REPROCESS"
        if target_file.exists()
        else "INITIAL"
    )

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

        if watermark is not None:
            rows = [
                row
                for row in rows
                if row[watermark_column] > watermark
            ]

        rows_read = len(rows)

        if rows:
            if load_type == "REPROCESS":
                write_mode = "w"
            else:
                write_mode = "a"

            file_exists = (
                target_file.exists()
                and target_file.stat().st_size > 0
            )

            with target_file.open(
                write_mode,
                newline="",
                encoding="utf-8",
            ) as file:
                fieldnames = rows[0].keys()

                writer = csv.DictWriter(
                    file,
                    fieldnames=fieldnames,
                )

                if write_mode == "w" or not file_exists:
                    writer.writeheader()

                writer.writerows(rows)

        rows_written = rows_read

        if rows and watermark_column in rows[0]:
            watermark_end = max(
                row[watermark_column]
                for row in rows
            )

            save_watermark(
                entity=entity,
                watermark_column=watermark_column,
                watermark_value=watermark_end,
                updated_at=datetime.now().isoformat(),
            )

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