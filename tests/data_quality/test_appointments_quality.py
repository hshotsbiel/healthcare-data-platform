import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

PATIENTS_FILE = (
    BASE_DIR
    / "data"
    / "sample"
    / "patients.csv"
)

APPOINTMENTS_FILE = (
    BASE_DIR
    / "data"
    / "sample"
    / "appointments.csv"
)


def test_appointments_reference_existing_patients():
    with PATIENTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        patients = list(csv.DictReader(file))

    with APPOINTMENTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        appointments = list(csv.DictReader(file))

    patient_ids = {
        row["patient_id"]
        for row in patients
    }

    appointment_patient_ids = {
        row["patient_id"]
        for row in appointments
    }

    invalid_patient_ids = (
        appointment_patient_ids - patient_ids
    )

    assert invalid_patient_ids == set()