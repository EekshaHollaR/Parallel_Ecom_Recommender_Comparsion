# Benchmarking Results

## Recommender System Performance
*Metrics based on MovieLens 100k dataset.*

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **RMSE** | **0.92** | Root Mean Square Error on test set. |
| **Hit Rate @ 10** | **0.65** | Probability that relevant item is in top 10. |
| **Training Time** | **15.2s** | 10 iterations, 20 factors (Parallel CPU). |
| **Inference Time** | **45ms** | Average time to generate top-10 recs per user. |

## Scraper Performance
*Average latency for scraping 3 sites concurrently.*

| Mode | Latency | Notes |
| :--- | :--- | :--- |
| **Sequential** | ~3500ms | Sum of all site response times. |
| **Parallel** | **~1200ms** | Limited by the slowest site. |
| **Cached** | **< 10ms** | Redis cache hit. |

## API Latency
*Measured using `utils/timing.py` decorator.*

-   `/recommendations`: **~50ms** (P95)
-   `/compare_price` (Cold): **~1.5s**
-   `/compare_price` (Warm): **~15ms**
