def success_response(data, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data,
        "latency_ms": 0  # Placeholder, will be filled by timing decorator
    }

def error_response(message, code=400):
    return {
        "status": "error",
        "message": message,
        "data": None
    }, code
