import csv
from pathlib import Path


PATIENTS_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample"
    / "patients.csv"
)


def test_patients_have_unique_ids():
    with PATIENTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    patient_ids = [
        row["patient_id"]
        for row in rows
    ]

    assert len(patient_ids) == len(set(patient_ids))


def test_patients_have_required_fields():
    required_fields = [
        "patient_id",
        "first_name",
        "last_name",
        "birth_date",
        "gender",
    ]

    with PATIENTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        for field in required_fields:
            assert row[field] is not None
            assert row[field].strip() != ""