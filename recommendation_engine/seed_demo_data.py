"""Populates data/items.json and data/users.json with sample records.

Run this once before your demo/screenshots so option 5 (Get recommendations)
has something interesting to show immediately:

    python seed_demo_data.py
    python main.py
"""

from models import Item, UserProfile
from engine import RecommendationEngine
from strategies import JaccardSimilarityStrategy
from storage import DataManager

SAMPLE_ITEMS = [
    Item("B1", "Dune", "Book", ["scifi", "adventure", "politics"]),
    Item("B2", "Foundation", "Book", ["scifi", "politics"]),
    Item("B3", "Pride and Prejudice", "Book", ["romance", "classic"]),
    Item("B4", "The Hobbit", "Book", ["adventure", "fantasy"]),
    Item("M1", "Inception", "Movie", ["scifi", "thriller"]),
    Item("M2", "The Notebook", "Movie", ["romance", "drama"]),
]

SAMPLE_USERS = [
    UserProfile("U1", "Ada", liked_attributes=["scifi", "adventure"]),
    UserProfile("U2", "Ben", liked_attributes=["romance", "classic"]),
]


def main() -> None:
    engine = RecommendationEngine(JaccardSimilarityStrategy())
    for item in SAMPLE_ITEMS:
        engine.add_item(item)
    for user in SAMPLE_USERS:
        engine.add_user(user)

    manager = DataManager("data/items.json", "data/users.json")
    manager.save_items(engine.items)
    manager.save_users(engine.users)
    print(f"Seeded {len(engine.items)} items and {len(engine.users)} users into data/.")


if __name__ == "__main__":
    main()
