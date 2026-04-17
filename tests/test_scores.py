"""
Unit tests for the scores persistence module.
"""

import unittest
import os
import json
import tempfile

import src.scores as scores_module


class ScoresTests(unittest.TestCase):
    """Unit tests for the scores persistence module."""

    def setUp(self):
        # Redirect the module to a fresh temp file for each test
        self._tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w")
        self._tmp.write("{}")
        self._tmp.close()
        self._orig_path = scores_module._SCORES_FILE
        scores_module._SCORES_FILE = self._tmp.name

    def tearDown(self):
        scores_module._SCORES_FILE = self._orig_path
        os.unlink(self._tmp.name)

    def test_get_best_time_returns_none_when_empty(self):
        self.assertIsNone(scores_module.get_best_time("normal"))

    def test_record_time_stores_value(self):
        scores_module.record_time("normal", 42)
        self.assertEqual(scores_module.get_best_time("normal"), 42)

    def test_record_time_returns_true_on_first_entry(self):
        result = scores_module.record_time("easy", 30)
        self.assertTrue(result)

    def test_record_time_returns_false_if_slower(self):
        scores_module.record_time("easy", 30)
        result = scores_module.record_time("easy", 50)
        self.assertFalse(result)

    def test_record_time_returns_true_if_faster(self):
        scores_module.record_time("easy", 50)
        result = scores_module.record_time("easy", 25)
        self.assertTrue(result)

    def test_only_top_five_kept(self):
        # Додаємо 6 результатів
        for t in [10, 20, 30, 40, 50, 60]:
            scores_module.record_time("hard", t)
            
        data = scores_module.load_scores()
        
        # Перевіряємо, що збереглося рівно 5 записів
        self.assertEqual(len(data["hard"]), 5)
        
        # Дістаємо час із нових словників і перевіряємо, чи збереглись топ-5
        times = [entry["time"] for entry in data["hard"]]
        self.assertEqual(times, [10, 20, 30, 40, 50])

    def test_different_difficulties_are_independent(self):
        scores_module.record_time("easy", 100)
        scores_module.record_time("hard", 200)
        self.assertEqual(scores_module.get_best_time("easy"), 100)
        self.assertEqual(scores_module.get_best_time("hard"), 200)

    def test_load_scores_returns_empty_on_corrupt_file(self):
        with open(self._tmp.name, "w") as f:
            f.write("NOT VALID JSON{{{")
        self.assertEqual(scores_module.load_scores(), {})

    def test_best_time_updates_after_new_record(self):
        scores_module.record_time("normal", 60)
        scores_module.record_time("normal", 30)
        self.assertEqual(scores_module.get_best_time("normal"), 30)


if __name__ == "__main__":
    unittest.main()