from pathlib import Path

from src.utils.ingestion import ingest_csv


def test_reprocess_does_not_duplicate_records(tmp_path, monkeypatch):
    source_file = tmp_path / "patients.csv"

    source_file.write_text(
        "patient_id,name\n"
        "P001,Ana Silva\n"
        "P002,João Santos\n",
        encoding="utf-8",
    )

    bronze_dir = tmp_path / "bronze"

    test_log_file = tmp_path / "ingestion_log.csv"

    monkeypatch.setattr(
        "src.utils.ingestion_logger.LOG_FILE",
        test_log_file,
    )

    first_result = ingest_csv(
        source_file=source_file,
        bronze_dir=bronze_dir,
        entity="patients",
        source="test",
        load_date="2026-10-08",
        run_id="test-run-001",
    )

    second_result = ingest_csv(
        source_file=source_file,
        bronze_dir=bronze_dir,
        entity="patients",
        source="test",
        load_date="2026-10-08",
        run_id="test-run-002",
    )

    target_file = (
        bronze_dir
        / "load_date=2026-10-08"
        / "patients.csv"
    )

    lines = target_file.read_text(
        encoding="utf-8",
    ).splitlines()

    assert first_result["load_type"] == "INITIAL"
    assert second_result["load_type"] == "REPROCESS"

    assert first_result["rows_read"] == 2
    assert second_result["rows_read"] == 2

    assert len(lines) == 3

    assert test_log_file.exists()