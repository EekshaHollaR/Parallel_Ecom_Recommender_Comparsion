# Parallel E-commerce Recommender & Price Comparison Engine

A high-performance, parallel AI-based recommendation system and multi-site price comparison engine.

## Features

- **Parallel ALS-NCG Recommender**: Matrix factorization using Alternating Least Squares with Non-linear Conjugate Gradient optimization. Supports multiprocessing and optional GPU acceleration.
- **Price Comparison Engine**: Multithreaded scraper to fetch and compare prices across sites.
- **Scalable Architecture**: Dockerized services with Redis caching and Celery task queue.
- **Modern Stack**: Python (Flask), React, Redis, Docker.

## Project Structure

```
root/
  backend/
    recommender/    # ALS-NCG Recommender logic (Parallel/GPU)
    scraper/        # Multithreaded price scraper
    api/            # Flask API endpoints
    utils/          # Shared utilities
    models/         # Database models
  frontend/         # React application
  docker/           # Docker configuration
  docs/             # Documentation
  tests/            # Unit and integration tests
```

## Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Node.js 16+

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repo_url>
    cd parallel-Ecommerce-Recommender-1.0
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```

3.  **Manual Setup (Dev):**

    *Backend:*
    ```bash
    cd backend
    pip install -r requirements.txt
    python app.py
    ```

    *Frontend:*
    ```bash
    cd frontend
    npm install
    npm start
    ```

## Recommender System Details

The recommender uses a hybrid parallel approach:
- **CPU**: `multiprocessing` for parallel ALS updates.
- **GPU**: Optional `numba` or `pycuda` acceleration if available.
- **Algorithm**: ALS-NCG (Alternating Least Squares with Non-linear Conjugate Gradient).
