from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Interaction, User, Product
import json

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track/view', methods=['POST'])
@jwt_required(optional=True)
def track_view():
    data = request.get_json()
    product_name = data.get('product_name')
    
    if not product_name:
        return jsonify({"error": "Missing product_name"}), 400

    user_identity = get_jwt_identity()
    user_id = None
    
    if user_identity:
        user = User.query.filter_by(username=user_identity).first()
        if user:
            user_id = user.id
    
    # In a real app, we'd resolve product_name to a product_id from our DB
    # For now, we just log the interaction with metadata
    
    interaction = Interaction(
        user_id=user_id if user_id else 0, # 0 for anonymous
        type='view',
        metadata_json=json.dumps({"product_name": product_name})
    )
    
    try:
        db.session.add(interaction)
        db.session.commit()
        return jsonify({"status": "recorded"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tracking_bp.route('/track/search', methods=['POST'])
@jwt_required(optional=True)
def track_search():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "Missing query"}), 400

    user_identity = get_jwt_identity()
    user_id = None
    
    if user_identity:
        user = User.query.filter_by(username=user_identity).first()
        if user:
            user_id = user.id

    interaction = Interaction(
        user_id=user_id if user_id else 0,
        type='search',
        metadata_json=json.dumps({"query": query})
    )
    
    try:
        db.session.add(interaction)
        db.session.commit()
        return jsonify({"status": "recorded"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
