from pathlib import Path
import csv


BASE_DIR = Path(__file__).resolve().parents[2]

WATERMARK_FILE = (
    BASE_DIR
    / "data"
    / "control"
    / "watermark.csv"
)

FIELDNAMES = [
    "entity",
    "watermark_column",
    "watermark_value",
    "updated_at",
]


def get_watermark(
    entity: str,
) -> dict | None:
    if not WATERMARK_FILE.exists():
        return None

    with WATERMARK_FILE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        if row["entity"] == entity:
            return row

    return None


def save_watermark(
    entity: str,
    watermark_column: str,
    watermark_value: str,
    updated_at: str,
):
    WATERMARK_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    if WATERMARK_FILE.exists():
        with WATERMARK_FILE.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as file:
            rows = list(csv.DictReader(file))

    updated = False

    for row in rows:
        if row["entity"] == entity:
            row["watermark_column"] = watermark_column
            row["watermark_value"] = watermark_value
            row["updated_at"] = updated_at
            updated = True
            break

    if not updated:
        rows.append(
            {
                "entity": entity,
                "watermark_column": watermark_column,
                "watermark_value": watermark_value,
                "updated_at": updated_at,
            }
        )

    with WATERMARK_FILE.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES,
        )

        writer.writeheader()
        writer.writerows(rows)