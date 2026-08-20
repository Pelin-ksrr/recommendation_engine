"""Interactive command-line interface for the Simple Recommendation Engine."""

from models import Item, UserProfile
from engine import RecommendationEngine
from strategies import JaccardSimilarityStrategy, WeightedAttributeStrategy
from storage import DataManager
from exceptions import RecommendationEngineError

ITEMS_PATH = "data/items.json"
USERS_PATH = "data/users.json"

MENU = """
==== Simple Recommendation Engine ====
1. Add item
2. Add user
3. List items
4. List users
5. Get recommendations
6. Switch scoring strategy
7. Save & Exit
0. Exit without saving
"""


def prompt_nonempty(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This field cannot be empty, please try again.")


def add_item_flow(engine: RecommendationEngine) -> None:
    try:
        item_id = prompt_nonempty("Item ID: ")
        title = prompt_nonempty("Title: ")
        category = prompt_nonempty("Category: ")
        attrs_raw = input("Attributes (comma separated): ").strip()
        attributes = [a.strip() for a in attrs_raw.split(",") if a.strip()]
        item = Item(item_id=item_id, title=title, category=category, attributes=attributes)
        engine.add_item(item)
        print(f"Item '{title}' added.")
    except RecommendationEngineError as exc:
        print(f"Error: {exc}")


def add_user_flow(engine: RecommendationEngine) -> None:
    try:
        user_id = prompt_nonempty("User ID: ")
        name = prompt_nonempty("Name: ")
        liked_raw = input("Liked attributes (comma separated): ").strip()
        liked = [a.strip() for a in liked_raw.split(",") if a.strip()]
        user = UserProfile(user_id=user_id, name=name, liked_attributes=liked)
        engine.add_user(user)
        print(f"User '{name}' added.")
    except RecommendationEngineError as exc:
        print(f"Error: {exc}")


def list_items_flow(engine: RecommendationEngine) -> None:
    if not engine.items:
        print("No items yet.")
        return
    for item in sorted(engine.items.values(), key=lambda i: i.title):
        attrs = ", ".join(item.attributes) if item.attributes else "-"
        print(f"- [{item.item_id}] {item.title} ({item.category}) — {attrs}")


def list_users_flow(engine: RecommendationEngine) -> None:
    if not engine.users:
        print("No users yet.")
        return
    for user in sorted(engine.users.values(), key=lambda u: u.name):
        liked = ", ".join(user.liked_attributes) if user.liked_attributes else "-"
        print(f"- [{user.user_id}] {user.name} — likes: {liked}")


def recommend_flow(engine: RecommendationEngine) -> None:
    try:
        user_id = prompt_nonempty("User ID: ")
        top_n_raw = input("How many recommendations? [5]: ").strip()
        top_n = int(top_n_raw) if top_n_raw else 5
        results = engine.recommend(user_id, top_n=top_n)
        if not results:
            print("No matching recommendations found for this user yet.")
            return
        print(f"\nTop {len(results)} recommendation(s):")
        for rank, r in enumerate(results, start=1):
            item = r["item"]
            reasons = ", ".join(r["reasons"]) if r["reasons"] else "general match"
            print(f"{rank}. {item.title} (score={r['score']}) — because: {reasons}")
    except RecommendationEngineError as exc:
        print(f"Error: {exc}")
    except ValueError:
        print("Please enter a valid whole number.")


def switch_strategy_flow(engine: RecommendationEngine) -> None:
    print(f"Current strategy: {engine.strategy.name}")
    print("1. Jaccard similarity\n2. Weighted attribute")
    choice = input("Choose: ").strip()
    if choice == "1":
        engine.set_strategy(JaccardSimilarityStrategy())
        print("Switched to Jaccard similarity.")
    elif choice == "2":
        engine.set_strategy(WeightedAttributeStrategy())
        print("Switched to weighted attribute scoring.")
    else:
        print("Invalid choice, strategy unchanged.")


def main() -> None:
    manager = DataManager(ITEMS_PATH, USERS_PATH)
    engine = RecommendationEngine(JaccardSimilarityStrategy())
    try:
        engine.items = manager.load_items()
        engine.users = manager.load_users()
        print(f"Loaded {len(engine.items)} item(s) and {len(engine.users)} user(s).")
    except RecommendationEngineError as exc:
        print(f"Warning: could not load saved data ({exc}). Starting with an empty catalog.")

    while True:
        print(MENU)
        choice = input("Select: ").strip()
        if choice == "1":
            add_item_flow(engine)
        elif choice == "2":
            add_user_flow(engine)
        elif choice == "3":
            list_items_flow(engine)
        elif choice == "4":
            list_users_flow(engine)
        elif choice == "5":
            recommend_flow(engine)
        elif choice == "6":
            switch_strategy_flow(engine)
        elif choice == "7":
            try:
                manager.save_items(engine.items)
                manager.save_users(engine.users)
                print("Saved. Goodbye!")
            except RecommendationEngineError as exc:
                print(f"Error while saving: {exc}")
            break
        elif choice == "0":
            print("Exiting without saving.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
