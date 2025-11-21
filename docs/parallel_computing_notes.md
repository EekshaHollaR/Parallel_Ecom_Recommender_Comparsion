# Parallel Computing Notes

## Alternating Least Squares (ALS) with NCG
The core recommendation engine uses **Alternating Least Squares (ALS)** to factorize the user-item interaction matrix $R$ into two lower-rank matrices:
-   $U$: User Factors ($M \times K$)
-   $V$: Item Factors ($N \times K$)

The optimization problem is solved by fixing one matrix (e.g., $V$) and solving for the other ($U$) using regularized least squares, then alternating.

### Parallelization Strategy (CPU)
Since the update for each user $u$ (or item $i$) is independent of other users (or items) when the other matrix is fixed, we can parallelize the updates.

**Implementation:** `backend/recommender/parallel_engine.py`

1.  **Batching**: Users/Items are split into batches.
2.  **Executor**: We use `concurrent.futures.ThreadPoolExecutor` (or `ProcessPoolExecutor` on Linux) to process batches in parallel.
3.  **Linear Algebra**: Each thread solves the linear system $A x = b$:
    $$ (V^T V + \lambda I) u_u^T = V^T R_u^T $$
    Where $R_u$ is the row of ratings for user $u$.

> **Note on Windows**: We use `ThreadPoolExecutor` by default on Windows to avoid `multiprocessing` pickling overhead and spawn issues. On Linux/Unix, `ProcessPoolExecutor` can be used for true parallelism bypassing the GIL for pure NumPy operations.

### GPU Acceleration (Optional)
For very large datasets, CPU parallelism may hit bottlenecks. We provide an optional GPU engine using **Numba/CUDA**.

**Implementation:** `backend/recommender/gpu_engine.py`

-   **Data Transfer**: Matrices $U$, $V$, and $R$ are transferred to GPU memory.
-   **Kernel**: A CUDA kernel computes the gradients and updates factors using **Stochastic Gradient Descent (SGD)** or parallel ALS steps.
-   **Requirement**: Requires an NVIDIA GPU and CUDA toolkit installed.

## Scraper Parallelism
The price scraper uses I/O-bound parallelism.

**Implementation:** `backend/scraper/scraper.py`

-   **Threading**: Uses `ThreadPoolExecutor`.
-   **Mechanism**: Spawns a thread for each target website (Amazon, eBay, Walmart, etc.).
-   **Benefit**: Total latency is roughly equal to the latency of the slowest site, rather than the sum of all sites.
