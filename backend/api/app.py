import sys
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Add backend to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.recommender.als_ncg import ALSRecommender
from backend.scraper.scraper import PriceScraper
from backend.api.routes.recommendations import recommendations_bp
from backend.api.routes.price_compare import price_compare_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production
    jwt = JWTManager(app)

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from backend.api.models import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Initialize Services
    print("=" * 80)
    print("Initializing Recommender...")
    print("=" * 80)
    # Use n_jobs=4 for parallelism
    recommender = ALSRecommender(n_factors=10, max_iter=5, n_jobs=4)
    # Train on dummy data for demo purposes
    dummy_data = [
        (0, 0, 5.0), (0, 1, 3.0), (0, 2, 4.0),
        (1, 0, 4.0), (1, 1, 1.0), (1, 3, 5.0),
        (2, 1, 2.0), (2, 2, 5.0), (2, 4, 3.0)
    ]
    recommender.fit(dummy_data)
    app.config['RECOMMENDER'] = recommender
    
    print("=" * 80)
    print("Initializing Scraper...")
    print("=" * 80)
    scraper = PriceScraper()
    app.config['SCRAPER'] = scraper
    
    # Register Blueprints
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(price_compare_bp)
    
    from backend.api.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from backend.api.routes.tracking import tracking_bp
    app.register_blueprint(tracking_bp)
    
    # INLINE RECOMMENDATIONS ROUTE (bypassing blueprint to debug)
    @app.route('/recommendations_direct', methods=['GET'])
    def get_recommendations_direct():
        print("=" * 80)
        print("DIRECT RECOMMENDATIONS ROUTE CALLED!")
        print("=" * 80)
        
        from flask import request
        
        # Get parameters
        user_id = request.args.get('user_id', type=int)
        n_top = request.args.get('n', type=int, default=5)
        
        print(f"user_id={user_id}, n_top={n_top}")
        
        # Access global recommender from app context
        recommender = app.config.get('RECOMMENDER')
        
        print(f"recommender={recommender}")
        
        if not recommender:
            return {"status": "error", "message": "Recommender service unavailable"}, 503
            
        try:
            # Predict using Hybrid Engine
            print(f"Calling recommender.predict with user_id={user_id}, n_top={n_top}")
            recs = recommender.predict(user_id, n_top=n_top)
            
            print(f"Got {len(recs)} recommendations")
            
            # Format response (recs is already a list of dicts)
            data = {
                "user_id": user_id,
                "recommendations": recs
            }
            return {"status": "success", "message": "Success", "data": data}
            
        except Exception as e:
            print(f"Error in get_recommendations_direct: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": str(e)}, 500
    
    @app.route('/test')
    def test_route():
        print("=" * 80)
        print("TEST ROUTE CALLED!")
        print("=" * 80)
        return {"status": "test route works", "recommender": str(app.config.get('RECOMMENDER'))}
    
    @app.route('/health')
    def health():
        return {"status": "ok"}
    
    print("=" * 80)
    print("Flask app initialized successfully!")
    print("=" * 80)
        
    return app

if __name__ == '__main__':
    app = create_app()
    # Run without debug mode for cleaner output
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
