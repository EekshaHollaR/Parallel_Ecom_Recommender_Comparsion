import redis
import redis
import json
import os
from typing import Optional, Dict, Any

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

class ScraperCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, expiry: int = 600):
        self.expiry = expiry
        try:
            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.client.ping() # Check connection
            self.enabled = True
        except redis.ConnectionError:
            print("Warning: Redis not available. Caching disabled.")
            self.enabled = False

    def _get_key(self, site: str, product: str) -> str:
        return f"price:{site}:{product.lower().replace(' ', '_')}"

    def get_cached_price(self, site: str, product: str) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None
        
        key = self._get_key(site, product)
        try:
            data = self.client.get(key)
            if data:
                self.client.incr('metrics:cache_hits')
                result = json.loads(data)
                result['source'] = 'cache'
                return result
            else:
                self.client.incr('metrics:cache_misses')
        except Exception as e:
            print(f"Cache read error: {e}")
            
        return None

    def cache_price(self, site: str, product: str, data: Dict[str, Any]) -> None:
        """Cache price for 10 minutes (600s) by default."""
        if not self.enabled:
            return
            
        key = self._get_key(site, product)
        try:
            self.client.setex(key, self.expiry, json.dumps(data))
        except Exception as e:
            print(f"Cache write error: {e}")

# Global instance
cache = ScraperCache(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
