import numpy as np
from sklearn.model_selection import train_test_split
import pickle
import os

class Preprocessor:
    """
    Handles data normalization and splitting.
    """
    
    @staticmethod
    def normalize_ratings(ratings: np.ndarray, strategy='minmax') -> np.ndarray:
        """
        Normalizes ratings.
        strategy: 'minmax' (0-1) or 'zscore' (mean 0, std 1)
        """
        if strategy == 'minmax':
            min_r = np.min(ratings)
            max_r = np.max(ratings)
            if max_r - min_r == 0:
                return ratings
            return (ratings - min_r) / (max_r - min_r)
        
        elif strategy == 'zscore':
            mean = np.mean(ratings)
            std = np.std(ratings)
            if std == 0:
                return ratings
            return (ratings - mean) / std
            
        return ratings

    @staticmethod
    def split_data(data, test_size=0.2, random_state=42):
        """
        Splits data (list of tuples or dataframe) into train and test sets.
        """
        return train_test_split(data, test_size=test_size, random_state=random_state)

    @staticmethod
    def save_processed_data(data, filepath):
        """Saves data using pickle."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def load_processed_data(filepath):
        """Loads data using pickle."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)

if __name__ == "__main__":
    # Test
    ratings = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    norm = Preprocessor.normalize_ratings(ratings)
    print(f"Normalized: {norm}")
