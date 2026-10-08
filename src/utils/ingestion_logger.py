from pathlib import Path
import csv
import time


BASE_DIR = Path(__file__).resolve().parents[2]

LOG_FILE = BASE_DIR / "data" / "control" / "ingestion_log.csv"
LOCK_DIR = BASE_DIR / "data" / "control" / "ingestion_log.lock"

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


def acquire_lock(timeout_seconds=30):
    start_time = time.time()

    while True:
        try:
            LOCK_DIR.mkdir()
            return

        except FileExistsError:
            if time.time() - start_time >= timeout_seconds:
                raise TimeoutError(
                    "Não foi possível adquirir o lock do "
                    "ingestion_log.csv dentro do tempo limite."
                )

            time.sleep(0.1)


def release_lock():
    if LOCK_DIR.exists():
        LOCK_DIR.rmdir()


def log_ingestion(result: dict):
    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    acquire_lock()

    try:
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

    finally:
        release_lock()