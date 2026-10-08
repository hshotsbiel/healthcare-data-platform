from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parents[2]

LOG_FILE = BASE_DIR / "data" / "control" / "ingestion_log.csv"

FIELDNAMES = [
    "run_id",
    "entity",
    "source",
    "load_date",
    "load_type",
    "status",
    "rows_read",
    "rows_written",
    "started_at",
    "finished_at",
    "error_message",
]


def log_ingestion(result: dict):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LOG_FILE.exists()

    with LOG_FILE.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(result)