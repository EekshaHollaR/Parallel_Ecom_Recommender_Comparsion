import os
import sys
import redis
from rq import Worker, Queue, Connection
from rq.decorators import job

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.recommender.als_ncg import ALSRecommender
from backend.scraper.scraper import PriceScraper

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
q = Queue(connection=redis_conn)

# We need to instantiate services here for the worker process
# In a real production setup, we might use a factory or singleton pattern more robustly
print("Worker initializing services...")
recommender = ALSRecommender(n_factors=10, max_iter=5)
# Train on dummy data
dummy_data = [
    (0, 0, 5.0), (0, 1, 3.0), (0, 2, 4.0),
    (1, 0, 4.0), (1, 1, 1.0), (1, 3, 5.0),
    (2, 1, 2.0), (2, 2, 5.0), (2, 4, 3.0)
]
recommender.fit(dummy_data)

scraper = PriceScraper()

def async_recommend(user_id, n_top=5):
    """Background task for generating recommendations."""
    print(f"Processing async recommendation for user {user_id}")
    try:
        recs = recommender.predict(user_id, n_top=n_top)
        return [
            {"item_id": int(item_id), "score": round(float(score), 4)} 
            for item_id, score in recs
        ]
    except Exception as e:
        print(f"Error in async_recommend: {e}")
        raise e

def async_compare_price(product_name):
    """Background task for scraping prices."""
    print(f"Processing async price comparison for {product_name}")
    try:
        return scraper.scrape_all(product_name)
    except Exception as e:
        print(f"Error in async_compare_price: {e}")
        raise e

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(['default'])
        worker.work()
