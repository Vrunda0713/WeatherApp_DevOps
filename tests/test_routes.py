import pytest
import json
from unittest.mock import patch, MagicMock
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ─── Route Tests ───────────────────────────────────────────────

def test_index_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_weather_no_city_returns_400(client):
    response = client.get('/weather')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data


def test_weather_short_city_returns_400(client):
    response = client.get('/weather?city=a')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data


def test_weather_city_not_found_returns_404(client):
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch('app.routes.requests.get', return_value=mock_response):
        response = client.get('/weather?city=InvalidCityXYZ')
        data = json.loads(response.data)
        assert response.status_code == 404
        assert 'error' in data


def test_weather_valid_city_returns_200(client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'name': 'Pune',
        'sys': {'country': 'IN'},
        'main': {
            'temp': 30.0,
            'feels_like': 32.0,
            'humidity': 60
        },
        'wind': {'speed': 5.0},
        'weather': [{'description': 'clear sky', 'icon': '01d', 'main': 'Clear'}]
    }

    with patch('app.routes.requests.get', return_value=mock_response):
        response = client.get('/weather?city=Pune')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['city'] == 'Pune'
        assert data['country'] == 'IN'
        assert data['temperature'] == 30
        assert data['humidity'] == 60
        assert 'wind_speed' in data
        assert 'description' in data


def test_weather_timeout_returns_504(client):
    import requests as req
    with patch('app.routes.requests.get', side_effect=req.exceptions.Timeout):
        response = client.get('/weather?city=Pune')
        data = json.loads(response.data)
        assert response.status_code == 504
        assert 'error' in data


def test_weather_connection_error_returns_503(client):
    import requests as req
    with patch('app.routes.requests.get', side_effect=req.exceptions.ConnectionError):
        response = client.get('/weather?city=Pune')
        data = json.loads(response.data)
        assert response.status_code == 503
        assert 'error' in data


def test_weather_invalid_api_key_returns_401(client):
    mock_response = MagicMock()
    mock_response.status_code = 401

    with patch('app.routes.requests.get', return_value=mock_response):
        response = client.get('/weather?city=Pune')
        data = json.loads(response.data)
        assert response.status_code == 401
        assert 'error' in data


def test_weather_response_has_all_fields(client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'name': 'Mumbai',
        'sys': {'country': 'IN'},
        'main': {'temp': 28.5, 'feels_like': 30.0, 'humidity': 75},
        'wind': {'speed': 3.5},
        'weather': [{'description': 'few clouds', 'icon': '02d', 'main': 'Clouds'}]
    }

    with patch('app.routes.requests.get', return_value=mock_response):
        response = client.get('/weather?city=Mumbai')
        data = json.loads(response.data)
        required_fields = ['city', 'country', 'temperature', 'feels_like',
                           'humidity', 'wind_speed', 'description', 'icon', 'condition']
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
