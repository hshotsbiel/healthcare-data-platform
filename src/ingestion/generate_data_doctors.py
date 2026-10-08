from pathlib import Path
import csv

from faker import Faker


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "sample"

fake = Faker("pt_BR")

SPECIALTIES = [
    "Cardiologia",
    "Clínica Médica",
    "Ortopedia",
    "Pediatria",
    "Neurologia",
    "Dermatologia",
    "Ginecologia",
    "Urologia",
    "Oftalmologia",
    "Oncologia",
]


def generate_doctors(quantity=30):
    doctors = []

    for number in range(1, quantity + 1):
        state = fake.estado_sigla()

        doctor = {
            "doctor_id": f"D{number:06d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "specialty": fake.random_element(
                elements=SPECIALTIES
            ),
            "license_number": (
                f"CRM-{state}-{fake.random_int(min=100000, max=999999)}"
            ),
            "state": state,
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now",
            ).isoformat(),
        }

        doctors.append(doctor)

    return doctors


def save_doctors(doctors):
    file_path = DATA_DIR / "doctors.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=doctors[0].keys(),
        )
        writer.writeheader()
        writer.writerows(doctors)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    doctors = generate_doctors()

    save_doctors(doctors)

    print(f"Médicos gerados: {len(doctors)}")
    print(f"Arquivo salvo em: {DATA_DIR / 'doctors.csv'}")


if __name__ == "__main__":
    main()