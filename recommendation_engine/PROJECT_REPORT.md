# Project Report — Simple Recommendation Engine

## Problem Understanding
The task asks for a system that recommends items to a user based on
attributes and preferences, with **explainable** matching — the result
must state why an item was recommended, not just a bare score. This
rules out opaque approaches and pushed the design toward a transparent,
rule-based scoring model.

## Proposed Approach
1. Model items and users as simple, serializable data classes.
2. Separate the *scoring algorithm* from the *engine that uses it*, so
   the matching logic can be swapped or extended without touching CRUD
   or persistence code (Strategy design pattern).
3. Keep every recommendation explainable by having each strategy return
   both a numeric score and the list of attributes that drove it.
4. Wrap all mutating operations (add/remove) in validation and custom
   exceptions so bad input never silently corrupts the catalog.
5. Persist to JSON so data survives between runs, with defensive error
   handling for missing/corrupted files.

## Implementation
- `models.py` — `Item` and `UserProfile` dataclasses with `to_dict` /
  `from_dict` for JSON (de)serialization.
- `strategies.py` — an abstract `ScoringStrategy` base class with two
  concrete implementations: `JaccardSimilarityStrategy` (overlap ratio)
  and `WeightedAttributeStrategy` (custom per-attribute weights).
- `engine.py` — `RecommendationEngine` holds the catalogs, performs
  validated CRUD, and produces a sorted, top-N, explainable
  recommendation list via whichever strategy is currently set.
- `storage.py` — `DataManager` loads/saves items and users as JSON,
  raising a single `StorageError` for any I/O or parsing failure.
- `exceptions.py` — a small hierarchy (`DuplicateItemError`,
  `ItemNotFoundError`, `InvalidDataError`, etc.) so the CLI can catch
  one base exception and still report specific, actionable messages.
- `cli.py` / `main.py` — a menu-driven console front end that wires the
  above together and handles all user I/O, keeping business logic out
  of the presentation layer.

## Important Technical Decisions
- **Strategy pattern over `if/elif` scoring logic** — chosen so a new
  scoring algorithm can be added as a new class implementing
  `ScoringStrategy`, without modifying `RecommendationEngine` at all.
  This was the main opportunity to demonstrate inheritance/polymorphism
  at more than a superficial level.
- **Dict-keyed catalogs (`item_id` → `Item`)** rather than lists, so
  duplicate detection and lookups are O(1) instead of O(n).
- **Explainability baked into the return type** (`score` + `reasons`)
  instead of bolted on afterward, since it was a core requirement of
  the project description, not a nice-to-have.
- **JSON over pickle/CSV** for persistence — human-readable, easy to
  inspect/debug during development, and adequate for the data volume
  involved here.

## Testing Performed
8 automated `unittest` cases (see `tests/test_engine.py`) covering
normal, boundary (no-match), duplicate, and invalid/missing-data
scenarios, all passing. In addition, the CLI was run manually end to
end — adding items and users, listing them, requesting recommendations
under both strategies, saving, and restarting the app to confirm the
saved JSON reloads correctly.

## Challenges Encountered
- Deciding how much of the "explainability" to surface without making
  the CLI output noisy — resolved by only listing the attributes that
  actually matched, rather than the full attribute sets.
- Making the two scoring strategies genuinely different (not just
  cosmetically), so switching strategies visibly changes the ranking
  for the same data — verified explicitly in the weighted-strategy test.

## Solutions Implemented
- Kept the `reasons` list strictly to matched attributes only.
- Added `test_weighted_strategy_scores_by_weight`, which asserts an
  exact expected score to prove the weighted strategy is doing real,
  distinct arithmetic rather than reusing the Jaccard result.

## Future Scope
See "Future Improvements" in `README.md`: semantic (embedding-based)
matching, an edit/update flow, report export, and a lightweight web UI
built on the same `RecommendationEngine` core.
