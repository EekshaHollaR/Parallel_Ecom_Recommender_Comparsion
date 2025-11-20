import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from .cache import cache

# Mock User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

class PriceScraper:
    def __init__(self):
        self.sites = [
            {"name": "Amazon", "base_url": "https://www.amazon.com/s?k="},
            {"name": "eBay", "base_url": "https://www.ebay.com/sch/i.html?_nkw="},
            {"name": "Walmart", "base_url": "https://www.walmart.com/search?q="},
            {"name": "BestBuy", "base_url": "https://www.bestbuy.com/site/searchpage.jsp?st="},
            {"name": "Target", "base_url": "https://www.target.com/s?searchTerm="}
        ]

    def _scrape_site(self, site, product_name):
        """
        Scrapes a single site.
        Note: This is a MOCK implementation since real scraping requires complex parsing/proxies.
        """
        # Check cache first
        cached_data = cache.get_cached_price(site['name'], product_name)
        if cached_data:
            cached_data['source'] = 'cache'
            return cached_data

        url = f"{site['base_url']}{product_name.replace(' ', '+')}"
        
        # Simulate network request
        try:
            # In a real scenario:
            # headers = {'User-Agent': random.choice(USER_AGENTS)}
            # response = requests.get(url, headers=headers, timeout=5)
            # soup = BeautifulSoup(response.text, 'html.parser')
            # parse logic...
            
            # Mock latency
            time.sleep(random.uniform(0.5, 2.0))
            
            # Mock result generation
            # 20% chance of failure/not found
            if random.random() < 0.2:
                return None
                
            # Generate a random realistic price based on product name hash
            seed = hash(product_name + site['name'])
            random.seed(seed)
            base_price = abs(hash(product_name)) % 500 + 10
            price = round(base_price * random.uniform(0.9, 1.1), 2)
            
            result = {
                "site": site['name'],
                "price": price,
                "currency": "USD",
                "product_url": url,
                "timestamp": datetime.now().isoformat(),
                "source": "live"
            }
            
            # Cache the result
            cache.cache_price(site['name'], product_name, result)
            
            return result
            
        except Exception as e:
            print(f"Error scraping {site['name']}: {e}")
            return None

    def scrape_all(self, product_name, max_workers=5):
        """
        Scrapes all configured sites concurrently.
        """
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_site = {executor.submit(self._scrape_site, site, product_name): site for site in self.sites}
            
            for future in as_completed(future_to_site):
                data = future.result()
                if data:
                    results.append(data)
                    
        latency = (time.time() - start_time) * 1000
        
        # Sort by price
        results.sort(key=lambda x: x['price'])
        
        return {
            "product": product_name,
            "results": results,
            "total_latency_ms": round(latency, 2),
            "sites_scraped": len(results)
        }

if __name__ == "__main__":
    scraper = PriceScraper()
    print("Scraping prices for 'Sony Headphones'...")
    data = scraper.scrape_all("Sony Headphones")
    print(json.dumps(data, indent=2))
