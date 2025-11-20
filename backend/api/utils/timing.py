import time
from functools import wraps

def measure_latency(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000
        
        # If result is a tuple (response, status_code), unpack it
        if isinstance(result, tuple):
            response, status = result
            if isinstance(response, dict):
                response['latency_ms'] = round(latency_ms, 2)
            return response, status
            
        # If result is a dict, add latency
        if isinstance(result, dict):
            result['latency_ms'] = round(latency_ms, 2)
            
        return result
    return decorated_function
