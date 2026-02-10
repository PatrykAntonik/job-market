"""
Load testing package (Locust personas, journeys, helpers).

This is intentionally lightweight; having `load_tests` as a package allows stable,
explicit imports (and avoids collisions with stdlib modules like `http`).
"""
