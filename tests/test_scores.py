import src.scores as scores_module


def test_load_scores_returns_empty_for_missing_file(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "missing-scores.json"
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    assert scores_module.load_scores() == {}


def test_load_scores_returns_empty_for_corrupt_file(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("NOT VALID JSON", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    assert scores_module.load_scores() == {}


def test_save_scores_persists_data(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))
    data = {"easy": [{"name": "Alice", "time": 15}]}

    scores_module.save_scores(data)

    assert scores_module.load_scores() == data


def test_get_best_time_returns_none_when_difficulty_has_no_results(
    monkeypatch,
    tmp_path,
) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    assert scores_module.get_best_time("normal") is None


def test_record_time_returns_true_for_first_entry(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    assert scores_module.record_time("easy", 30, "Alice") is True
    assert scores_module.get_best_time("easy") == 30


def test_record_time_returns_false_for_slower_time(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))
    scores_module.record_time("easy", 30, "Alice")

    assert scores_module.record_time("easy", 50, "Bob") is False
    assert scores_module.get_best_time("easy") == 30


def test_record_time_returns_true_for_new_best_time(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))
    scores_module.record_time("easy", 50, "Alice")

    assert scores_module.record_time("easy", 25, "Bob") is True
    assert scores_module.get_best_time("easy") == 25


def test_record_time_keeps_only_top_five_results(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    for index, elapsed in enumerate([45, 10, 30, 20, 60, 15], start=1):
        scores_module.record_time("hard", elapsed, f"Player {index}")

    entries = scores_module.load_scores()["hard"]

    assert len(entries) == 5
    assert [entry["time"] for entry in entries] == [10, 15, 20, 30, 45]


def test_record_time_stores_results_per_difficulty(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    scores_module.record_time("easy", 100, "Alice")
    scores_module.record_time("hard", 200, "Bob")

    assert scores_module.get_best_time("easy") == 100
    assert scores_module.get_best_time("hard") == 200


def test_get_leaderboard_migrates_old_integer_format(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text('{"easy": [40, 20, 30]}', encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    leaderboard = scores_module.get_leaderboard("easy")

    assert [entry["time"] for entry in leaderboard] == [20, 30, 40]
    assert all(entry["name"] for entry in leaderboard)
