from pathlib import Path
import csv

from faker import Faker


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "sample"

fake = Faker("pt_BR")


def generate_patients(quantity=100):
    patients = []

    for number in range(1, quantity + 1):
        patient = {
            "patient_id": f"P{number:06d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(
                minimum_age=0,
                maximum_age=100,
            ).isoformat(),
            "gender": fake.random_element(
                elements=("M", "F")
            ),
            "city": fake.city(),
            "state": fake.estado_sigla(),
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now",
            ).isoformat(),
        }

        patients.append(patient)

    return patients


def save_patients(patients):
    file_path = DATA_DIR / "patients.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=patients[0].keys(),
        )
        writer.writeheader()
        writer.writerows(patients)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    patients = generate_patients()

    save_patients(patients)

    print(f"Pacientes gerados: {len(patients)}")
    print(f"Arquivo salvo em: {DATA_DIR / 'patients.csv'}")


if __name__ == "__main__":
    main()