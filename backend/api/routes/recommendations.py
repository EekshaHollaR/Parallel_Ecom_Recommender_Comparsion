from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils.timing import measure_latency
from ..utils.schemas import success_response, error_response
import logging

logger = logging.getLogger(__name__)

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations', methods=['GET'])
@measure_latency
@jwt_required(optional=True)
def get_recommendations():
    print("=" * 80)
    print("GET_RECOMMENDATIONS CALLED!")
    print("=" * 80)
    logger.info("get_recommendations called")
    # Try to get user from JWT
    user_identity = get_jwt_identity()
    user_id = None
    
    if user_identity:
        from ..models import User
        user = User.query.filter_by(username=user_identity).first()
        if user:
            user_id = user.id
            
    # Fallback to query param for testing or anonymous
    if user_id is None:
        user_id = request.args.get('user_id', type=int)

    n_top = request.args.get('n', type=int, default=5)
    
    logger.info(f"user_id={user_id}, n_top={n_top}")
    
    # Access global recommender from app context
    recommender = current_app.config.get('RECOMMENDER')
    
    logger.info(f"recommender={recommender}")
    
    if not recommender:
        return error_response("Recommender service unavailable", 503)
        
    try:
        # Predict using Hybrid Engine
        logger.info(f"Calling recommender.predict with user_id={user_id}, n_top={n_top}")
        recs = recommender.predict(user_id, n_top=n_top)
        
        logger.info(f"Got {len(recs)} recommendations")
        
        # Format response (recs is already a list of dicts)
        data = {
            "user_id": user_id,
            "recommendations": recs
        }
        return success_response(data)
        
    except Exception as e:
        logger.error(f"Error in get_recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return error_response(str(e), 500)
