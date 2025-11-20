import pytest
import pandas as pd
import numpy as np
import os
from backend.recommender.dataset_loader import DatasetLoader

@pytest.fixture
def dummy_csv(tmp_path):
    d = tmp_path / "dummy.csv"
    d.write_text("1,101,5.0,123\n1,102,3.5,124\n2,101,4.0,125")
    return str(d)

def test_load_data(dummy_csv):
    loader = DatasetLoader(dummy_csv, names=['user_id', 'item_id', 'rating', 'timestamp'])
    df = loader.load_data()
    assert len(df) == 3
    assert 'user_id' in df.columns

def test_build_mappings(dummy_csv):
    loader = DatasetLoader(dummy_csv, names=['user_id', 'item_id', 'rating', 'timestamp'])
    loader.load_data()
    loader.build_mappings()
    
    assert loader.n_users == 2
    assert loader.n_items == 2
    assert 'user_idx' in loader.df.columns
    assert 'item_idx' in loader.df.columns

def test_interaction_matrix(dummy_csv):
    loader = DatasetLoader(dummy_csv, names=['user_id', 'item_id', 'rating', 'timestamp'])
    loader.load_data()
    matrix = loader.get_interaction_matrix()
    
    assert matrix.shape == (2, 2)
    # User 1 (idx 0) rated Item 101 (idx 0) as 5.0
    assert matrix[0, 0] == 5.0
