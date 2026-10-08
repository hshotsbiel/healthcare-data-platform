from pathlib import Path
import csv

from faker import Faker


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "sample"

fake = Faker("pt_BR")

PROCEDURES = [
    ("Consulta médica", "Ambulatorial"),
    ("Exame de sangue", "Diagnóstico"),
    ("Raio-X", "Diagnóstico"),
    ("Tomografia", "Diagnóstico"),
    ("Ressonância magnética", "Diagnóstico"),
    ("Ultrassonografia", "Diagnóstico"),
    ("Eletrocardiograma", "Diagnóstico"),
    ("Cirurgia", "Cirúrgico"),
    ("Endoscopia", "Diagnóstico"),
    ("Fisioterapia", "Terapêutico"),
]


def generate_procedures(quantity=300):
    procedures = []

    for number in range(1, quantity + 1):
        procedure_name, procedure_type = fake.random_element(
            elements=PROCEDURES
        )

        procedure = {
            "procedure_id": f"PR{number:06d}",
            "patient_id": f"P{fake.random_int(min=1, max=100):06d}",
            "doctor_id": f"D{fake.random_int(min=1, max=30):06d}",
            "hospital_id": f"H{fake.random_int(min=1, max=15):06d}",
            "procedure_name": procedure_name,
            "procedure_type": procedure_type,
            "procedure_date": fake.date_time_between(
                start_date="-1y",
                end_date="+30d",
            ).isoformat(),
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now",
            ).isoformat(),
        }

        procedures.append(procedure)

    return procedures


def save_procedures(procedures):
    file_path = DATA_DIR / "procedures.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=procedures[0].keys(),
        )
        writer.writeheader()
        writer.writerows(procedures)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    procedures = generate_procedures()

    save_procedures(procedures)

    print(f"Procedimentos gerados: {len(procedures)}")
    print(f"Arquivo salvo em: {DATA_DIR / 'procedures.csv'}")


if __name__ == "__main__":
    main()