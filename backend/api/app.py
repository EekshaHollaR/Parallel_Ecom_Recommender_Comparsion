import sys
import os
from flask import Flask
from flask_cors import CORS

# Add backend to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.recommender.als_ncg import ALSRecommender
from backend.scraper.scraper import PriceScraper
from backend.api.routes.recommendations import recommendations_bp
from backend.api.routes.price_compare import price_compare_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Initialize Services
    # In a real app, we'd load a pre-trained model
    print("Initializing Recommender...")
    recommender = ALSRecommender(n_factors=10, max_iter=5)
    # Train on dummy data for demo purposes
    dummy_data = [
        (0, 0, 5.0), (0, 1, 3.0), (0, 2, 4.0),
        (1, 0, 4.0), (1, 1, 1.0), (1, 3, 5.0),
        (2, 1, 2.0), (2, 2, 5.0), (2, 4, 3.0)
    ]
    recommender.fit(dummy_data)
    app.config['RECOMMENDER'] = recommender
    
    print("Initializing Scraper...")
    scraper = PriceScraper()
    app.config['SCRAPER'] = scraper
    
    # Register Blueprints
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(price_compare_bp)
    
    from backend.api.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    
    @app.route('/health')
    def health():
        return {"status": "ok"}
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
