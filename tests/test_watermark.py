from src.utils.watermark import (
    get_watermark,
    save_watermark,
)


def test_save_and_get_watermark(tmp_path, monkeypatch):
    test_watermark_file = (
        tmp_path / "watermark.csv"
    )

    monkeypatch.setattr(
        "src.utils.watermark.WATERMARK_FILE",
        test_watermark_file,
    )

    save_watermark(
        entity="patients",
        watermark_column="created_at",
        watermark_value="2026-10-05T08:00:00",
        updated_at="2026-10-08T18:00:00",
    )

    result = get_watermark("patients")

    assert result is not None
    assert result["entity"] == "patients"
    assert result["watermark_column"] == "created_at"
    assert result["watermark_value"] == "2026-10-05T08:00:00"
    assert result["updated_at"] == "2026-10-08T18:00:00"


def test_get_watermark_returns_none_for_unknown_entity(
    tmp_path,
    monkeypatch,
):
    test_watermark_file = (
        tmp_path / "watermark.csv"
    )

    monkeypatch.setattr(
        "src.utils.watermark.WATERMARK_FILE",
        test_watermark_file,
    )

    result = get_watermark("unknown_entity")

    assert result is None


def test_save_watermark_updates_existing_entity(
    tmp_path,
    monkeypatch,
):
    test_watermark_file = (
        tmp_path / "watermark.csv"
    )

    monkeypatch.setattr(
        "src.utils.watermark.WATERMARK_FILE",
        test_watermark_file,
    )

    save_watermark(
        entity="patients",
        watermark_column="created_at",
        watermark_value="2026-10-05T08:00:00",
        updated_at="2026-10-08T18:00:00",
    )

    save_watermark(
        entity="patients",
        watermark_column="created_at",
        watermark_value="2026-10-06T08:00:00",
        updated_at="2026-10-09T18:00:00",
    )

    result = get_watermark("patients")

    assert result is not None
    assert result["watermark_value"] == "2026-10-06T08:00:00"
    assert result["updated_at"] == "2026-10-09T18:00:00"

    lines = test_watermark_file.read_text(
        encoding="utf-8",
    ).splitlines()

    assert len(lines) == 2