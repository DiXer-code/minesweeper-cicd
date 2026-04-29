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
    data = {"easy": [15, 20]}

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

    assert scores_module.record_time("easy", 30) is True
    assert scores_module.get_best_time("easy") == 30


def test_record_time_returns_false_for_slower_time(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))
    scores_module.record_time("easy", 30)

    assert scores_module.record_time("easy", 50) is False
    assert scores_module.get_best_time("easy") == 30


def test_record_time_returns_true_for_new_best_time(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))
    scores_module.record_time("easy", 50)

    assert scores_module.record_time("easy", 25) is True
    assert scores_module.get_best_time("easy") == 25


def test_record_time_keeps_only_three_fastest_results(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    for elapsed in [45, 10, 30, 20, 60]:
        scores_module.record_time("hard", elapsed)

    assert scores_module.load_scores()["hard"] == [10, 20, 30]


def test_record_time_stores_results_per_difficulty(monkeypatch, tmp_path) -> None:
    scores_file = tmp_path / "scores.json"
    scores_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(scores_module, "_SCORES_FILE", str(scores_file))

    scores_module.record_time("easy", 100)
    scores_module.record_time("hard", 200)

    assert scores_module.get_best_time("easy") == 100
    assert scores_module.get_best_time("hard") == 200
