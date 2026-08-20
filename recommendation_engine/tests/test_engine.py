"""Unit tests for the Simple Recommendation Engine.

Run with:  python -m pytest tests/  (or)  python -m unittest discover tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Item, UserProfile
from engine import RecommendationEngine
from strategies import JaccardSimilarityStrategy, WeightedAttributeStrategy
from exceptions import (
    DuplicateItemError,
    ItemNotFoundError,
    DuplicateUserError,
    UserNotFoundError,
    InvalidDataError,
)


class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RecommendationEngine(JaccardSimilarityStrategy())
        self.engine.add_item(Item("B1", "Dune", "Book", ["scifi", "adventure"]))
        self.engine.add_item(Item("B2", "Foundation", "Book", ["scifi", "politics"]))
        self.engine.add_item(Item("B3", "Pride and Prejudice", "Book", ["romance", "classic"]))
        self.engine.add_user(UserProfile("U1", "Ada", liked_attributes=["scifi", "adventure"]))

    # 1. Normal case: matching items are ranked with reasons
    def test_recommend_returns_ranked_matches(self):
        results = self.engine.recommend("U1")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["item"].item_id, "B1")
        self.assertIn("scifi", results[0]["reasons"])

    # 2. Boundary case: user with no attribute overlap gets an empty list, not an error
    def test_recommend_no_match_returns_empty(self):
        self.engine.add_user(UserProfile("U2", "Ben", liked_attributes=["horror"]))
        results = self.engine.recommend("U2")
        self.assertEqual(results, [])

    # 3. Duplicate-data case: re-adding an existing item id is rejected
    def test_duplicate_item_raises(self):
        with self.assertRaises(DuplicateItemError):
            self.engine.add_item(Item("B1", "Dune (dup)", "Book", ["scifi"]))

    # 4. Missing/invalid-data case: item without a title is rejected
    def test_missing_title_raises_invalid_data(self):
        with self.assertRaises(InvalidDataError):
            self.engine.add_item(Item("B9", "", "Book", ["scifi"]))

    # 5. Invalid input case: recommending for a non-existent user raises
    def test_recommend_for_unknown_user_raises(self):
        with self.assertRaises(UserNotFoundError):
            self.engine.recommend("NOPE")

    # 6. Duplicate-data case: re-adding an existing user id is rejected
    def test_duplicate_user_raises(self):
        with self.assertRaises(DuplicateUserError):
            self.engine.add_user(UserProfile("U1", "Ada again"))

    # 7. Boundary case: removing a non-existent item raises rather than failing silently
    def test_remove_unknown_item_raises(self):
        with self.assertRaises(ItemNotFoundError):
            self.engine.remove_item("NOPE")

    # 8. Alternate strategy case: weighted scoring reflects custom weights (polymorphism)
    def test_weighted_strategy_scores_by_weight(self):
        self.engine.set_strategy(WeightedAttributeStrategy())
        self.engine.users["U1"].weights = {"scifi": 5.0, "adventure": 1.0}
        results = self.engine.recommend("U1")
        self.assertEqual(results[0]["item"].item_id, "B1")
        self.assertAlmostEqual(results[0]["score"], 6.0)


if __name__ == "__main__":
    unittest.main()
