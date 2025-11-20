import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def solve_chunk(chunk_indices, fixed_matrix, ratings_matrix, regularization):
    """
    Solves for a chunk of vectors (users or items) using Least Squares.
    
    Args:
        chunk_indices: Indices of vectors to update in this chunk.
        fixed_matrix: The other factor matrix (e.g., Item matrix V when updating User matrix U).
        ratings_matrix: The sparse ratings matrix (users x items or items x users).
        regularization: Regularization parameter (lambda).
        
    Returns:
        List of tuples (index, new_vector)
    """
    # Precompute XtX + lambda * I
    YtY = fixed_matrix.T @ fixed_matrix
    lambda_I = regularization * np.eye(YtY.shape[0])
    
    results = []
    
    # For each vector in the chunk
    for idx in chunk_indices:
        # Get ratings for this user/item
        # ratings_matrix is expected to be indexable by [idx, :] returning a sparse row/col
        # For efficiency, we assume ratings_matrix is passed in a way that allows fast access
        # Or we pass the specific ratings data for this chunk.
        
        # Simplified: assuming dense row access or pre-sliced data is better for IPC
        # But for this example, we'll assume we have access to the data.
        # In a real large-scale system, we'd use shared memory or pass only non-zero entries.
        
        # Let's assume ratings_matrix is a dense row/col for simplicity in this snippet,
        # or a sparse representation.
        
        # To make it truly parallel friendly without huge serialization overhead, 
        # we usually pass the raw data needed.
        pass 
        
    # NOTE: Passing the entire ratings_matrix to subprocesses is inefficient.
    # A better approach for `multiprocessing` is to use `shared_memory` or pass only the necessary data.
    # However, for the sake of this "laptop-friendly" request, we will implement a 
    # simpler version where we solve linear systems using numpy's lstsq or solve.
    
    return results

def update_user_factors_parallel(U, V, ratings, regularization, n_jobs=-1):
    """
    Parallel update of user factors.
    """
    n_users, n_factors = U.shape
    if n_jobs == -1:
        n_jobs = multiprocessing.cpu_count()
        
    # Precompute V.T @ V + lambda * I
    VtV = V.T @ V
    lambda_I = regularization * np.eye(n_factors)
    
    # We can use a ProcessPool, but for simple numpy operations, 
    # sometimes threadpool is enough if BLAS releases GIL.
    # However, requested is multiprocessing.
    
    # To avoid serialization costs, we'll use a shared memory approach or 
    # just iterate in parallel if the data isn't too massive.
    # For this implementation, we'll stick to a direct solver per user 
    # but optimized with batching if possible.
    
    # Actually, a pure python loop with numpy is slow. 
    # Let's define a worker function that takes a subset of users and their ratings.
    
    # Optimization: The standard ALS update for user u is:
    # u_i = inv(V.T @ V + lambda * I) @ V.T @ R_u
    # This assumes all items are rated, which is wrong for sparse data.
    # For implicit/explicit feedback with missing values treated as unknown (not zero),
    # we only sum over rated items.
    # u_i = inv(V_rated.T @ V_rated + lambda * I) @ V_rated.T @ r_u
    
    # This requires a different matrix inversion per user! Very expensive.
    # Parallelization is key here.
    
    return _parallel_als_step(U, V, ratings, regularization, n_jobs, is_user=True)

def update_item_factors_parallel(U, V, ratings, regularization, n_jobs=-1):
    return _parallel_als_step(V, U, ratings.T, regularization, n_jobs, is_user=False)

def _solve_batch(args):
    """
    Worker function to solve a batch of linear systems.
    """
    indices, fixed_matrix, ratings_csr, regularization = args
    n_factors = fixed_matrix.shape[1]
    lambda_I = regularization * np.eye(n_factors)
    
    new_vectors = np.zeros((len(indices), n_factors))
    
    for i, idx in enumerate(indices):
        # Get indices of items rated by this user (or users who rated this item)
        # ratings_csr is a scipy.sparse.csr_matrix
        start_ptr = ratings_csr.indptr[idx]
        end_ptr = ratings_csr.indptr[idx+1]
        
        if start_ptr == end_ptr:
            continue
            
        cols = ratings_csr.indices[start_ptr:end_ptr]
        data = ratings_csr.data[start_ptr:end_ptr]
        
        # Select rows from fixed_matrix corresponding to rated items
        V_subset = fixed_matrix[cols, :]
        
        # A = V_subset.T @ V_subset + lambda * I
        # b = V_subset.T @ ratings
        
        A = V_subset.T @ V_subset + lambda_I
        b = V_subset.T @ data
        
        # Solve Ax = b
        x = np.linalg.solve(A, b)
        new_vectors[i] = x
        
    return indices, new_vectors

def _parallel_als_step(Update_Matrix, Fixed_Matrix, ratings_csr, regularization, n_jobs, is_user):
    from scipy.sparse import csr_matrix
    
    n_targets = Update_Matrix.shape[0]
    
    # Split indices into chunks
    chunk_size = (n_targets + n_jobs - 1) // n_jobs
    chunks = []
    for i in range(0, n_targets, chunk_size):
        end = min(i + chunk_size, n_targets)
        chunks.append(range(i, end))
        
    # Prepare args
    # Note: Passing large matrices to processes is costly. 
    # In production, use SharedMemory. Here, we rely on OS copy-on-write (fork) on Linux/Mac,
    # but on Windows (spawn), this pickles data. 
    # For a "laptop-friendly" version, we will accept the overhead or suggest ThreadPool 
    # if the matrix is small enough, but the prompt asked for multiprocessing.
    
    # To make it work efficiently on Windows, we'd need to dump matrices to a file or use shared_memory.
    # For simplicity in this demo, we'll pass the data.
    
    tasks = [(chunk, Fixed_Matrix, ratings_csr, regularization) for chunk in chunks]
    
    new_matrix = np.zeros_like(Update_Matrix)
    
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        results = executor.map(_solve_batch, tasks)
        
    for indices, vectors in results:
        new_matrix[indices] = vectors
        
    return new_matrix
