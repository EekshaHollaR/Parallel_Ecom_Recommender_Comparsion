import pytest
import numpy as np
from backend.recommender.als_ncg import ALSRecommender

def test_als_initialization():
    model = ALSRecommender(n_factors=5, max_iter=2)
    assert model.n_factors == 5
    assert model.U is None

def test_als_fit_predict():
    data = [
        (0, 0, 5.0), (0, 1, 3.0),
        (1, 0, 4.0), (1, 1, 1.0),
        (2, 1, 2.0), (2, 2, 5.0)
    ]
    
    model = ALSRecommender(n_factors=2, max_iter=2)
    model.fit(data)
    
    assert model.U.shape == (3, 2)
    assert model.V.shape == (3, 2)
    
    recs = model.predict(0, n_top=2)
    assert len(recs) == 2
    assert isinstance(recs[0], tuple)
    
def test_predict_invalid_user():
    model = ALSRecommender()
    # Mock trained state
    model.U = np.random.rand(3, 2)
    model.V = np.random.rand(3, 2)
    
    # Should raise error if model not trained (checked via U is None)
    # But here we mocked it. 
    # If we pass index out of bounds for numpy array, it raises IndexError
    with pytest.raises(IndexError):
        model.predict(10)
