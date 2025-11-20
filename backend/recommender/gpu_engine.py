import numpy as np
import warnings

# Try importing Numba
try:
    from numba import jit, cuda, prange
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

class GPUEngine:
    def __init__(self):
        self.enabled = False
        if HAS_NUMBA and cuda.is_available():
            self.enabled = True
            print("GPU Acceleration Enabled (Numba/CUDA)")
        else:
            print("GPU Acceleration Unavailable. Using CPU.")

    def matrix_factorization_step(self, U, V, ratings_coo, regularization):
        """
        Perform one step of ALS or Gradient Descent on GPU.
        For ALS, exact solution on GPU is complex due to variable size systems.
        We often use SGD or CCD (Cyclic Coordinate Descent) on GPU.
        
        Here we'll implement a Numba-accelerated SGD step as a fallback/alternative 
        to the exact ALS solver, or a parallelized ALS if possible.
        """
        if not self.enabled:
            raise RuntimeError("GPU not available")
            
        # Example: Simple SGD update on GPU
        # This is just a placeholder for the complex ALS logic
        return self._sgd_update(U, V, ratings_coo.row, ratings_coo.col, ratings_coo.data, regularization)

    @staticmethod
    def _sgd_update(U, V, rows, cols, data, reg, lr=0.01, epochs=1):
        if not HAS_NUMBA:
            return U, V
            
        @cuda.jit
        def sgd_kernel(U, V, rows, cols, data, lr, reg):
            idx = cuda.grid(1)
            if idx < rows.shape[0]:
                u_idx = rows[idx]
                v_idx = cols[idx]
                rating = data[idx]
                
                # Dot product
                prediction = 0.0
                for k in range(U.shape[1]):
                    prediction += U[u_idx, k] * V[v_idx, k]
                    
                error = rating - prediction
                
                # Update
                for k in range(U.shape[1]):
                    u_val = U[u_idx, k]
                    v_val = V[v_idx, k]
                    
                    U[u_idx, k] += lr * (error * v_val - reg * u_val)
                    V[v_idx, k] += lr * (error * u_val - reg * v_val)

        # Copy to device
        d_U = cuda.to_device(U)
        d_V = cuda.to_device(V)
        d_rows = cuda.to_device(rows)
        d_cols = cuda.to_device(cols)
        d_data = cuda.to_device(data)
        
        threadsperblock = 256
        blockspergrid = (rows.shape[0] + (threadsperblock - 1)) // threadsperblock
        
        for _ in range(epochs):
            sgd_kernel[blockspergrid, threadsperblock](d_U, d_V, d_rows, d_cols, d_data, lr, reg)
            
        return d_U.copy_to_host(), d_V.copy_to_host()

if __name__ == "__main__":
    engine = GPUEngine()
    if engine.enabled:
        # Test
        U = np.random.rand(10, 5)
        V = np.random.rand(20, 5)
        # Dummy COO data
        rows = np.array([0, 1, 2])
        cols = np.array([0, 1, 2])
        data = np.array([5.0, 3.0, 4.0])
        
        # This requires a proper COO matrix object or passing arrays
        # For the test we just call the internal method
        U_new, V_new = GPUEngine._sgd_update(U, V, rows, cols, data, 0.1)
        print("GPU Update Complete")
