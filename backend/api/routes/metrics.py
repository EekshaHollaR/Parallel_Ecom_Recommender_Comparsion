from flask import Blueprint, jsonify
import redis
import os
import time

metrics_bp = Blueprint('metrics', __name__)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
except:
    redis_client = None

@metrics_bp.route('/metrics', methods=['GET'])
def get_metrics():
    if not redis_client:
        return jsonify({"error": "Redis unavailable"}), 503

    # Get RPS (Requests Per Second)
    # We'll use a sliding window or just current second count
    current_timestamp = int(time.time())
    rps_key = f"metrics:rps:{current_timestamp}"
    rps = int(redis_client.get(rps_key) or 0)
    
    # Get Cache Stats
    hits = int(redis_client.get('metrics:cache_hits') or 0)
    misses = int(redis_client.get('metrics:cache_misses') or 0)
    total = hits + misses
    hit_rate = round((hits / total * 100), 2) if total > 0 else 0

    return jsonify({
        "rps": rps,
        "cache_hit_rate": hit_rate,
        "cache_hits": hits,
        "cache_misses": misses
    })
