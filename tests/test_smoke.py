
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_app_initialization(client):
    """Smoke test to verify the app initializes and serves the index page."""
    response = client.get('/')
    # Depending on your app structure, '/' might return 200 or 302 (redirect)
    # We just check it doesn't crash (500)
    assert response.status_code < 500
