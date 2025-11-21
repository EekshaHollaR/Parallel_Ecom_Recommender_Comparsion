# Developer Guide

## Code Style
-   **Python**: Follow **PEP 8**. Use `flake8` for linting and `black` for formatting.
-   **JavaScript**: Follow **Airbnb** style guide. Use `ESLint`.

## Project Structure
-   `backend/`: Python source code.
    -   `recommender/`: ALS logic, data loading.
    -   `scraper/`: Price scraping logic.
    -   `api/`: Flask routes and app.
-   `frontend/`: React application.
-   `tests/`: Pytest and Jest tests.
-   `docs/`: Documentation.

## Extending the System

### Adding a New Scraper Site
1.  Open `backend/scraper/scraper.py`.
2.  Add a new dictionary to the `self.sites` list in `__init__`:
    ```python
    {"name": "NewStore", "url": "https://newstore.com/search?q={}"}
    ```
3.  (Optional) Implement specific parsing logic in `_scrape_site` if the generic parser fails.

### Adding a New Recommender Algorithm
1.  Create a new file in `backend/recommender/` (e.g., `neural_collab.py`).
2.  Implement a class with a `fit(data)` and `predict(user_id)` method.
3.  Update `backend/api/app.py` to initialize your new class instead of `ALSRecommender`.

## Troubleshooting

### Redis Connection Error
-   **Error**: `redis.exceptions.ConnectionError`
-   **Fix**: Ensure Redis is running (`redis-server`). If using Docker, ensure the `redis` service is up and the hostname is correct (`redis` vs `localhost`).

### Multiprocessing on Windows
-   **Issue**: `BrokenPipeError` or `PicklingError`.
-   **Fix**: The project defaults to `ThreadPoolExecutor` on Windows in `parallel_engine.py`. Ensure you are not forcing `ProcessPoolExecutor` unless you wrap the entry point in `if __name__ == '__main__':`.
