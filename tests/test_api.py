import pytest
from backend.api.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json['status'] == 'ok'

def test_recommendations_missing_param(client):
    rv = client.get('/recommendations')
    assert rv.status_code == 400

def test_recommendations_valid(client):
    # Assuming dummy data in create_app has user 0
    rv = client.get('/recommendations?user_id=0')
    assert rv.status_code == 200
    assert rv.json['status'] == 'success'
    assert len(rv.json['data']['recommendations']) > 0

def test_compare_price_valid(client):
    # Mocking scraper would be better, but for integration test we can let it run (it mocks network anyway)
    rv = client.get('/compare_price?product=test')
    assert rv.status_code == 200
    assert rv.json['status'] == 'success'
    assert 'results' in rv.json['data']
