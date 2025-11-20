import redis
import json
import os

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

class ScraperCache:
    def __init__(self):
        try:
            self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
            self.client.ping() # Check connection
            self.enabled = True
        except redis.ConnectionError:
            print("Warning: Redis not available. Caching disabled.")
            self.enabled = False

    def _get_key(self, site, product_name):
        return f"price:{site}:{product_name.lower().replace(' ', '_')}"

    def get_cached_price(self, site, product_name):
        if not self.enabled:
            return None
        
        key = self._get_key(site, product_name)
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def cache_price(self, site, product_name, data, expiry=600):
        """Cache price for 10 minutes (600s) by default."""
        if not self.enabled:
            return
            
        key = self._get_key(site, product_name)
        self.client.setex(key, expiry, json.dumps(data))

# Global instance
cache = ScraperCache()
