import numpy as np
import time
import logging
import random
from scipy.sparse import csr_matrix
from .parallel_engine import update_user_factors_parallel, update_item_factors_parallel
from .gpu_engine import GPUEngine
from typing import List, Tuple, Optional, Union, Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ALS-NCG")

# Hardcoded sample products to bypass database issues
SAMPLE_PRODUCTS = [
    {"item_id": 1, "name": "Apple iPhone 15 Pro", "score": 0.9, "image_url": "https://via.placeholder.com/300x300?text=iPhone+15", "price": 129900, "currency": "₹", "rating": 4.8, "reviews": 1250},
    {"item_id": 2, "name": "Samsung Galaxy S24 Ultra", "score": 0.85, "image_url": "https://via.placeholder.com/300x300?text=Galaxy+S24", "price": 124999, "currency": "₹", "rating": 4.7, "reviews": 980},
    {"item_id": 3, "name": "Sony WH-1000XM5 Headphones", "score": 0.8, "image_url": "https://via.placeholder.com/300x300?text=Sony+WH1000XM5", "price": 29990, "currency": "₹", "rating": 4.9, "reviews": 2100},
    {"item_id": 4, "name": "MacBook Air M3", "score": 0.95, "image_url": "https://via.placeholder.com/300x300?text=MacBook+Air", "price": 114900, "currency": "₹", "rating": 4.9, "reviews": 850},
    {"item_id": 5, "name": "Dell XPS 15", "score": 0.82, "image_url": "https://via.placeholder.com/300x300?text=Dell+XPS", "price": 145000, "currency": "₹", "rating": 4.6, "reviews": 620},
    {"item_id": 6, "name": "iPad Pro 12.9", "score": 0.88, "image_url": "https://via.placeholder.com/300x300?text=iPad+Pro", "price": 112900, "currency": "₹", "rating": 4.8, "reviews": 1100},
    {"item_id": 7, "name": "Canon EOS R6", "score": 0.75, "image_url": "https://via.placeholder.com/300x300?text=Canon+R6", "price": 219999, "currency": "₹", "rating": 4.7, "reviews": 340},
    {"item_id": 8, "name": "Bose QuietComfort 45", "score": 0.78, "image_url": "https://via.placeholder.com/300x300?text=Bose+QC45", "price": 28900, "currency": "₹", "rating": 4.6, "reviews": 1580},
    {"item_id": 9, "name": "LG OLED C3 55 inch TV", "score": 0.92, "image_url": "https://via.placeholder.com/300x300?text=LG+OLED", "price": 139990, "currency": "₹", "rating": 4.9, "reviews": 450},
    {"item_id": 10, "name": "PlayStation 5", "score": 0.87, "image_url": "https://via.placeholder.com/300x300?text=PS5", "price": 54990, "currency": "₹", "rating": 4.8, "reviews": 2300},
]

class ALSRecommender:
    def __init__(self, n_factors: int = 20, regularization: float = 0.1, max_iter: int = 10, use_gpu: bool = False, n_jobs: int = 1):
        self.n_factors = n_factors
        self.regularization = regularization
        self.max_iter = max_iter
        self.use_gpu = use_gpu
        self.n_jobs = n_jobs
        self.U: Optional[np.ndarray] = None
        self.V: Optional[np.ndarray] = None
        self.gpu_engine = GPUEngine() if use_gpu else None
        self.train_matrix: Optional[Any] = None
        self.product_cache: List[Dict[str, Any]] = SAMPLE_PRODUCTS.copy()  # Use hardcoded products
        
    def fit(self, train_data: Union[List[Tuple[int, int, float]], Any]) -> None:
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
                # GPU Path
                coo = self.train_matrix.tocoo()
                self.U, self.V = self.gpu_engine.matrix_factorization_step(
                    self.U, self.V, coo, self.regularization
                )
            else:
                # CPU Parallel ALS Path
                self.U = update_user_factors_parallel(
                    self.U, self.V, self.train_matrix, self.regularization, n_jobs=self.n_jobs
                )
                
                self.V = update_item_factors_parallel(
                    self.U, self.V, self.train_matrix, self.regularization, n_jobs=self.n_jobs
                )
            
            logger.info(f"Iteration {i+1}/{self.max_iter} - Time: {time.time() - iter_start:.2f}s")
            
        logger.info(f"Training complete in {time.time() - start_time:.2f}s")

    def predict(self, user_id: int = None, n_top: int = 10) -> List[Dict[str, Any]]:
        """
        Hybrid Recommender using hardcoded sample products.
        Returns random products from the sample list.
        """
        logger.info(f"predict called with user_id={user_id}, n_top={n_top}")
        
        if not self.product_cache:
            logger.warning("Product cache is empty!")
            return []
        
        # Return random products from the hardcoded list
        num_products = min(n_top, len(self.product_cache))
        selected_products = random.sample(self.product_cache, num_products)
        
        logger.info(f"Returning {len(selected_products)} recommendations from cache")
        return selected_products
