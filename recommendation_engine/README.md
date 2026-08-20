# Simple Recommendation Engine

## Problem Statement
Build a system that recommends items (e.g. books or movies) to a user based
on the item's attributes and the user's stated preferences, using an
explainable matching approach rather than a black-box score.

## Objective
Provide a console application where an operator can maintain a catalog of
items and a set of user profiles, and generate a ranked, explainable list
of recommendations for any given user — with the reasoning ("why") shown
alongside each result.

## Features
- Add items (id, title, category, attributes) with duplicate/validation checks
- Add user profiles (id, name, liked attributes, optional per-attribute weights)
- List all items / all users
- Generate top-N ranked recommendations for a user, filtered by category if desired
- Explainable output: each recommendation shows *which* attributes matched
- Two interchangeable scoring strategies (Strategy design pattern):
  - **Jaccard similarity** — overlap ratio between item and user attributes
  - **Weighted attribute** — score driven by custom per-attribute weights
- Persistent storage in JSON, reloaded automatically on startup
- Centralized exception handling for invalid input, duplicates, missing
  records and corrupted/unreadable data files

## Technologies Used
- Python 3 (standard library only — no paid APIs, no third-party packages)
- `dataclasses`, `abc` (abstract base classes), `json`, `unittest`

## Installation / Setup Instructions
No installation is required beyond a standard Python 3 interpreter
(3.8+). No external packages need to be installed.

```bash
git clone <this-repo>   # or unzip the submitted archive
cd recommendation_engine
```

## How to Run
```bash
# (optional) pre-populate sample data so recommendations have something to show
python seed_demo_data.py

# run the interactive application
python main.py
```
Follow the on-screen numbered menu to add items/users and request
recommendations. Choose option `7` to save your data before exiting.

To run the automated tests:
```bash
python -m unittest discover tests -v
```

## Project Structure
```
recommendation_engine/
├── main.py             # entry point
├── cli.py              # interactive menu / user interaction layer
├── engine.py           # RecommendationEngine: CRUD + ranking logic
├── strategies.py       # ScoringStrategy base class + 2 implementations
├── models.py           # Item and UserProfile data classes
├── storage.py          # JSON persistence (DataManager)
├── exceptions.py       # custom exception hierarchy
├── seed_demo_data.py   # optional sample-data generator for demos
├── data/               # created at runtime (items.json, users.json)
├── tests/
│   └── test_engine.py  # 8 unittest test cases
├── README.md
└── PROJECT_REPORT.md
```

## Testing Details
`tests/test_engine.py` contains 8 unittest cases covering:
1. Normal case — ranked recommendations with correct reasons
2. Boundary case — user with no attribute overlap gets an empty result
3. Duplicate item ID rejected
4. Missing required field (empty title) rejected
5. Recommending for an unknown user raises a clear error
6. Duplicate user ID rejected
7. Removing a non-existent item raises a clear error
8. Alternate (weighted) strategy produces a different, correct score

All 8 tests pass (`python -m unittest discover tests -v`). The CLI was
also manually exercised end-to-end (add items/users, list, recommend,
save, reload) to confirm persistence works correctly across runs.

## Limitations
- Matching is attribute/keyword-based, not semantic — items must share
  literal attribute tags to be matched.
- Single-user, single-machine, local JSON storage (no concurrent access
  or multi-user server).
- No authentication; anyone running the CLI can edit any profile.

## Future Improvements
- Add a TF-IDF or embedding-based similarity strategy for semantic matching
- Add an `edit`/`update` flow for existing items and users
- Export recommendation reports to CSV/Markdown
- Add a simple web UI on top of the same `RecommendationEngine` class
