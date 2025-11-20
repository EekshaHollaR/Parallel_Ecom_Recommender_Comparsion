import pytest
from unittest.mock import patch, MagicMock
from backend.scraper.scraper import PriceScraper

@pytest.fixture
def scraper():
    return PriceScraper()

def test_scraper_initialization(scraper):
    assert len(scraper.sites) > 0

@patch('backend.scraper.scraper.cache')
def test_scrape_site_cached(mock_cache, scraper):
    mock_cache.get_cached_price.return_value = {'price': 100, 'source': 'cache'}
    
    result = scraper._scrape_site(scraper.sites[0], "test product")
    assert result['price'] == 100
    assert result['source'] == 'cache'

def test_scrape_all(scraper):
    # Mock _scrape_site to avoid network calls and wait times
    with patch.object(scraper, '_scrape_site') as mock_scrape:
        mock_scrape.side_effect = [
            {'site': 'Amazon', 'price': 100},
            {'site': 'eBay', 'price': 90},
            None, None, None
        ]
        
        result = scraper.scrape_all("test product", max_workers=2)
        
        assert result['product'] == "test product"
        assert len(result['results']) == 2
        assert result['results'][0]['price'] == 90 # Sorted by price
