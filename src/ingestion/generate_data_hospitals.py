from pathlib import Path
import csv

from faker import Faker


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "sample"

fake = Faker("pt_BR")

HOSPITAL_TYPES = [
    "Hospital Geral",
    "Hospital Especializado",
    "Hospital Universitário",
]


def generate_hospitals(quantity=15):
    hospitals = []

    for number in range(1, quantity + 1):
        hospital = {
            "hospital_id": f"H{number:06d}",
            "hospital_name": (
                f"Hospital {fake.last_name()} "
                f"{fake.random_element(elements=('São Paulo', 'Central', 'Vida', 'Santa Casa', 'Regional'))}"
            ),
            "city": fake.city(),
            "state": fake.estado_sigla(),
            "hospital_type": fake.random_element(
                elements=HOSPITAL_TYPES
            ),
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now",
            ).isoformat(),
        }

        hospitals.append(hospital)

    return hospitals


def save_hospitals(hospitals):
    file_path = DATA_DIR / "hospitals.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=hospitals[0].keys(),
        )
        writer.writeheader()
        writer.writerows(hospitals)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    hospitals = generate_hospitals()

    save_hospitals(hospitals)

    print(f"Hospitais gerados: {len(hospitals)}")
    print(f"Arquivo salvo em: {DATA_DIR / 'hospitals.csv'}")


if __name__ == "__main__":
    main()