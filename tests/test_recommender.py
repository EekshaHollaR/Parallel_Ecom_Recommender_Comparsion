import sys
import os
import numpy as np

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from recommender.als_ncg import ALSRecommender

def test_simple_recommender():
    print("Running simple recommender test...")
    # Dummy data: 3 users, 3 items
    # User 0 likes Item 0 and 1
    # User 1 likes Item 0
    # User 2 likes Item 2
    data = [
        (0, 0, 5.0), (0, 1, 4.0),
        (1, 0, 4.0),
        (2, 2, 5.0)
    ]
    
    model = ALSRecommender(n_factors=2, max_iter=5, use_gpu=False)
    model.fit(data)
    
    recs = model.predict(0, n_top=2)
    print(f"Recommendations for User 0: {recs}")
    
    # Check shapes
    assert model.U.shape == (3, 2)
    assert model.V.shape == (3, 2)
    print("Test passed!")

if __name__ == "__main__":
    test_simple_recommender()
