import time
import random
import logging
from flask import current_app
from ..api.models import Product

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PriceScraper")

class PriceScraper:
    def __init__(self):
        self.sites = [
            {"name": "Amazon.in", "url": "https://www.amazon.in"},
            {"name": "Flipkart", "url": "https://www.flipkart.com"},
            {"name": "Croma", "url": "https://www.croma.com"}
        ]

    def scrape_all(self, product_name):
        """
        Simulates scraping by querying the local database of 50k+ items.
        Returns realistic variations for different stores.
        """
        start_time = time.time()
        results = []
        
        logger.info(f"Scraping for: {product_name}")
        
        # Search in local DB
        try:
            # Ensure we are in app context
            if not current_app:
                logger.error("No app context for database query")
                return {"product": product_name, "results": [], "total_latency_ms": 0}

            search_term = f"%{product_name}%"
            # Find best match (limit to 1 for "Best Deal" logic, or more if we want variety)
            # We'll get a few matches to simulate different products found
            db_products = Product.query.filter(Product.name.ilike(search_term)).limit(3).all()
            
            if not db_products:
                # Fallback: Try to find something in the same category if specific name fails
                # This makes the demo robust
                logger.info("No direct match, trying broad search")
                parts = product_name.split()
                if parts:
                    search_term = f"%{parts[0]}%"
                    db_products = Product.query.filter(Product.name.ilike(search_term)).limit(3).all()

            if db_products:
                base_product = db_products[0] # Use the best match as the "canonical" product
                
                for site in self.sites:
                    # Simulate network latency
                    time.sleep(random.uniform(0.1, 0.5))
                    
                    # Simulate price variation (Amazon usually cheaper, etc.)
                    price_variation = random.uniform(0.9, 1.1)
                    if site['name'] == "Amazon.in":
                        price_variation = random.uniform(0.85, 1.0)
                    elif site['name'] == "Flipkart":
                        price_variation = random.uniform(0.9, 1.05)
                    
                    simulated_price = round(base_product.price * price_variation, 2)
                    
                    results.append({
                        "site": site['name'],
                        "price": simulated_price,
                        "image_url": base_product.image_url,
                        "rating": base_product.rating,
                        "reviews": base_product.reviews,
                        "product_url": base_product.product_url,
                        "currency": "₹",
                        "name": base_product.name, # The name might slightly differ on sites in reality
                        "source": "simulation"
                    })
            
        except Exception as e:
            logger.error(f"Database search failed: {str(e)}")

        # Sort by price
        results.sort(key=lambda x: x['price'])
        
        total_latency = (time.time() - start_time) * 1000
        return {
            "product": product_name,
            "results": results,
            "total_latency_ms": round(total_latency, 2)
        }
