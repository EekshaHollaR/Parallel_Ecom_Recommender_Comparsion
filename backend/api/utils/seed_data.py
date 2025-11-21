import random
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.api.app import create_app
from backend.api.models import db, Product

app = create_app()

CATEGORIES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Camera", "Tablet", "Monitor", "Speaker"],
    "Fashion": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Dress", "Watch", "Sunglasses", "Handbag"],
    "Home": ["Sofa", "Lamp", "Table", "Chair", "Bed", "Rug", "Curtains", "Vase"],
    "Beauty": ["Lipstick", "Perfume", "Shampoo", "Cream", "Serum", "Mascara", "Eyeliner", "Blush"]
}

BRANDS = {
    "Electronics": ["Sony", "Apple", "Samsung", "Dell", "HP", "Bose", "JBL", "Canon", "Nikon", "Asus"],
    "Fashion": ["Nike", "Adidas", "Zara", "H&M", "Levi's", "Gucci", "Puma", "Reebok", "Uniqlo", "Gap"],
    "Home": ["IKEA", "Pepperfry", "Urban Ladder", "Home Centre", "Sleepwell", "Duroflex"],
    "Beauty": ["Lakme", "Maybelline", "L'Oreal", "Nivea", "Olay", "Dove", "MAC", "Clinique"]
}

ADJECTIVES = ["Premium", "Ultra", "Pro", "Max", "Lite", "Classic", "Modern", "Vintage", "Sleek", "Durable", "Stylish", "Comfortable", "Luxury", "Affordable", "Best-Selling", "Top-Rated"]

IMAGES = {
    "Electronics": "https://via.placeholder.com/300x300?text=Electronics",
    "Fashion": "https://via.placeholder.com/300x300?text=Fashion",
    "Home": "https://via.placeholder.com/300x300?text=Home",
    "Beauty": "https://via.placeholder.com/300x300?text=Beauty"
}

HERO_PRODUCTS = [
    {"name": "Apple iPhone 15 (128 GB) - Black", "category": "Electronics", "price": 79900, "image": "https://m.media-amazon.com/images/I/71657TiFeHL._SX679_.jpg"},
    {"name": "Samsung Galaxy S24 Ultra 5G AI Smartphone", "category": "Electronics", "price": 129999, "image": "https://m.media-amazon.com/images/I/71CXhVhpM0L._SX679_.jpg"},
    {"name": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones", "category": "Electronics", "price": 29990, "image": "https://m.media-amazon.com/images/I/51SKmu2G9FL._SX679_.jpg"},
    {"name": "MacBook Air M2 Chip", "category": "Electronics", "price": 99900, "image": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SX679_.jpg"},
    {"name": "Nike Air Jordan 1 Low", "category": "Fashion", "price": 8995, "image": "https://static.nike.com/a/images/t_PDP_1728_v1/f_auto,q_auto:eco/572c5e8c-566a-4476-9876-021593772121/air-jordan-1-low-shoes-459b4T.png"},
]

def generate_products(n=50000):
    print(f"Generating {n} products...")
    products = []
    
    # Add Hero Products first
    for hero in HERO_PRODUCTS:
        product = Product(
            name=hero['name'],
            price=hero['price'],
            image_url=hero['image'],
            rating=4.8,
            reviews=random.randint(500, 5000),
            category=hero['category'],
            description=f"Premium {hero['name']} with advanced features.",
            source_site="Catalog",
            product_url="http://example.com/hero"
        )
        products.append(product)
    
    for i in range(n):
        category = random.choice(list(CATEGORIES.keys()))
        item = random.choice(CATEGORIES[category])
        brand = random.choice(BRANDS[category])
        adj = random.choice(ADJECTIVES)
        
        name = f"{brand} {adj} {item} {random.randint(100, 999)}"
        price = round(random.uniform(500, 150000), 2)
        rating = round(random.uniform(3.0, 5.0), 1)
        reviews = random.randint(10, 5000)
        
        # 30% chance of being a "Catalog" item (real-ish)
        if random.random() < 0.3:
            source = "Catalog"
        else:
            source = random.choice(["Amazon", "Flipkart", "Croma"])

        product = Product(
            name=name,
            price=price,
            image_url=IMAGES[category],
            rating=rating,
            reviews=reviews,
            category=category,
            description=f"This is a great {item} from {brand}. Features include {adj} design and high quality materials.",
            source_site=source,
            product_url=f"http://example.com/product/{i}"
        )
        products.append(product)
        
        if i % 1000 == 0:
            print(f"Generated {i} items...")

    return products

def seed_db():
    with app.app_context():
        print("Dropping old tables...")
        db.drop_all()
        print("Creating new tables...")
        db.create_all()
        
        products = generate_products(50000)
        
        print("Bulk inserting into database...")
        # Batch insert for performance
        batch_size = 5000
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            db.session.bulk_save_objects(batch)
            db.session.commit()
            print(f"Committed batch {i//batch_size + 1}")
            
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
