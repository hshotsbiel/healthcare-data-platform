from pathlib import Path
import csv

from faker import Faker


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "sample"

fake = Faker("pt_BR")

APPOINTMENT_STATUSES = [
    "Agendada",
    "Realizada",
    "Cancelada",
    "Não compareceu",
]


def generate_appointments(quantity=500):
    appointments = []

    for number in range(1, quantity + 1):
        appointment = {
            "appointment_id": f"A{number:06d}",
            "patient_id": f"P{fake.random_int(min=1, max=100):06d}",
            "doctor_id": f"D{fake.random_int(min=1, max=30):06d}",
            "hospital_id": f"H{fake.random_int(min=1, max=15):06d}",
            "appointment_date": fake.date_time_between(
                start_date="-1y",
                end_date="+30d",
            ).isoformat(),
            "status": fake.random_element(
                elements=APPOINTMENT_STATUSES
            ),
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now",
            ).isoformat(),
        }

        appointments.append(appointment)

    return appointments


def save_appointments(appointments):
    file_path = DATA_DIR / "appointments.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=appointments[0].keys(),
        )
        writer.writeheader()
        writer.writerows(appointments)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    appointments = generate_appointments()

    save_appointments(appointments)

    print(f"Consultas geradas: {len(appointments)}")
    print(f"Arquivo salvo em: {DATA_DIR / 'appointments.csv'}")


if __name__ == "__main__":
    main()