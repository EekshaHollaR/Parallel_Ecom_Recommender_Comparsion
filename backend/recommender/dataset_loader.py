import pandas as pd
import numpy as np
import os
from typing import Tuple, Dict, Optional

class DatasetLoader:
    """
    Loads and processes rating data for the recommender system.
    Supports MovieLens-style (user_id, item_id, rating) CSVs.
    """
    
    def __init__(self, file_path: str, sep: str = ',', names: list = None):
        self.file_path = file_path
        self.sep = sep
        self.names = names or ['user_id', 'item_id', 'rating', 'timestamp']
        self.df = None
        self.n_users = 0
        self.n_items = 0
        self.user_map = {}
        self.item_map = {}
        self.reverse_user_map = {}
        self.reverse_item_map = {}

    def load_data(self) -> pd.DataFrame:
        """Loads data from CSV."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
            
        self.df = pd.read_csv(self.file_path, sep=self.sep, names=self.names, engine='python')
        
        # Drop missing values
        self.df.dropna(subset=['user_id', 'item_id', 'rating'], inplace=True)
        
        # Ensure types
        self.df['rating'] = self.df['rating'].astype(float)
        
        return self.df

    def build_mappings(self):
        """Maps user and item IDs to continuous integers."""
        if self.df is None:
            self.load_data()
            
        unique_users = self.df['user_id'].unique()
        unique_items = self.df['item_id'].unique()
        
        self.n_users = len(unique_users)
        self.n_items = len(unique_items)
        
        self.user_map = {u: i for i, u in enumerate(unique_users)}
        self.item_map = {i: idx for idx, i in enumerate(unique_items)}
        
        self.reverse_user_map = {v: k for k, v in self.user_map.items()}
        self.reverse_item_map = {v: k for k, v in self.item_map.items()}
        
        # Apply mappings
        self.df['user_idx'] = self.df['user_id'].map(self.user_map)
        self.df['item_idx'] = self.df['item_id'].map(self.item_map)

    def get_interaction_matrix(self) -> np.ndarray:
        """Returns a dense user-item matrix (use with caution for large datasets)."""
        if self.df is None or 'user_idx' not in self.df.columns:
            self.build_mappings()
            
        matrix = np.zeros((self.n_users, self.n_items))
        for row in self.df.itertuples():
            matrix[row.user_idx, row.item_idx] = row.rating
            
        return matrix

    def get_sparse_interaction_list(self) -> list:
        """Returns list of (user_idx, item_idx, rating) tuples."""
        if self.df is None or 'user_idx' not in self.df.columns:
            self.build_mappings()
            
        return list(zip(self.df['user_idx'], self.df['item_idx'], self.df['rating']))

if __name__ == "__main__":
    # Example usage
    # Create a dummy file for testing
    with open("dummy_ratings.csv", "w") as f:
        f.write("1,101,5.0,123456\n1,102,3.5,123457\n2,101,4.0,123458")
        
    loader = DatasetLoader("dummy_ratings.csv", names=['user_id', 'item_id', 'rating', 'timestamp'])
    loader.load_data()
    loader.build_mappings()
    print(f"Users: {loader.n_users}, Items: {loader.n_items}")
    print(loader.get_interaction_matrix())
    
    os.remove("dummy_ratings.csv")
