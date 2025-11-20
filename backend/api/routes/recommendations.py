from flask import Blueprint, request, current_app
from ..utils.timing import measure_latency
from ..utils.schemas import success_response, error_response

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations', methods=['GET'])
@measure_latency
def get_recommendations():
    user_id = request.args.get('user_id', type=int)
    n_top = request.args.get('n', type=int, default=5)
    
    if user_id is None:
        return error_response("Missing user_id parameter")
        
    # Access global recommender from app context
    recommender = current_app.config.get('RECOMMENDER')
    
    if not recommender:
        return error_response("Recommender service unavailable", 503)
        
    # Check for async mode
    mode = request.args.get('mode')
    if mode == 'async':
        from ..tasks.worker import q, async_recommend
        job = q.enqueue(async_recommend, user_id, n_top)
        return success_response({
            "job_id": job.get_id(),
            "status_url": f"/tasks/{job.get_id()}"
        }, message="Job enqueued")

    try:
        # Check if user exists (simple check)
        if user_id >= recommender.U.shape[0]:
             return error_response("User ID not found", 404)

        recs = recommender.predict(user_id, n_top=n_top)
        
        # Format response
        data = {
            "user_id": user_id,
            "recommendations": [
                {"item_id": int(item_id), "score": round(float(score), 4)} 
                for item_id, score in recs
            ]
        }
        return success_response(data)
        
    except Exception as e:
        return error_response(str(e), 500)
