import numpy as np
import time
import logging
from scipy.sparse import csr_matrix
from .parallel_engine import update_user_factors_parallel, update_item_factors_parallel
from .gpu_engine import GPUEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ALS-NCG")

class ALSRecommender:
    def __init__(self, n_factors=20, regularization=0.1, max_iter=10, use_gpu=False):
        self.n_factors = n_factors
        self.regularization = regularization
        self.max_iter = max_iter
        self.use_gpu = use_gpu
        self.U = None
        self.V = None
        self.gpu_engine = GPUEngine() if use_gpu else None
        
    def fit(self, train_data):
        """
        Train the model using ALS.
        train_data: List of (user, item, rating) tuples or a sparse matrix.
        """
        logger.info("Initializing model...")
        
        # Convert to sparse matrix if needed
        if isinstance(train_data, list):
            users, items, ratings = zip(*train_data)
            n_users = max(users) + 1
            n_items = max(items) + 1
            self.train_matrix = csr_matrix((ratings, (users, items)), shape=(n_users, n_items))
        else:
            self.train_matrix = train_data
            
        n_users, n_items = self.train_matrix.shape
        
        # Initialize factors randomly
        self.U = np.random.normal(scale=1./self.n_factors, size=(n_users, self.n_factors))
        self.V = np.random.normal(scale=1./self.n_factors, size=(n_items, self.n_factors))
        
        logger.info(f"Training on {n_users} users and {n_items} items.")
        
        start_time = time.time()
        
        for i in range(self.max_iter):
            iter_start = time.time()
            
            if self.use_gpu and self.gpu_engine and self.gpu_engine.enabled:
                # GPU Path (using SGD approximation for this demo, or exact ALS if implemented)
                # Converting CSR to COO for GPU
                coo = self.train_matrix.tocoo()
                self.U, self.V = self.gpu_engine.matrix_factorization_step(
                    self.U, self.V, coo, self.regularization
                )
            else:
                # CPU Parallel ALS Path
                # 1. Update Users
                self.U = update_user_factors_parallel(
                    self.U, self.V, self.train_matrix, self.regularization
                )
                
                # 2. Update Items
                self.V = update_item_factors_parallel(
                    self.U, self.V, self.train_matrix, self.regularization
                )
            
            # Calculate Loss (Optional, expensive)
            # loss = self.calculate_loss()
            # logger.info(f"Iteration {i+1}/{self.max_iter} - Loss: {loss:.4f} - Time: {time.time() - iter_start:.2f}s")
            logger.info(f"Iteration {i+1}/{self.max_iter} - Time: {time.time() - iter_start:.2f}s")
            
        logger.info(f"Training complete in {time.time() - start_time:.2f}s")

    def predict(self, user_idx, n_top=10):
        """
        Predict top N items for a user.
        """
        if self.U is None or self.V is None:
            raise ValueError("Model not trained.")
            
        # Calculate scores for all items: u . V^T
        scores = self.U[user_idx] @ self.V.T
        
        # Get top N indices
        top_indices = np.argsort(scores)[::-1][:n_top]
        top_scores = scores[top_indices]
        
        return list(zip(top_indices, top_scores))

    def calculate_loss(self):
        """
        Calculate RMSE loss.
        """
        # This is expensive to compute on the whole matrix every iteration
        # Use a sample or skip for performance
        pass

if __name__ == "__main__":
    # Simple test
    data = [
        (0, 0, 5.0), (0, 1, 3.0),
        (1, 0, 4.0), (1, 1, 1.0),
        (2, 1, 2.0), (2, 2, 5.0)
    ]
    
    model = ALSRecommender(n_factors=5, max_iter=5)
    model.fit(data)
    
    recs = model.predict(0, n_top=2)
    print(f"Recommendations for User 0: {recs}")
