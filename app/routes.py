from flask import Blueprint, render_template, request, jsonify
import requests
import os

main = Blueprint('main', __name__)

API_KEY = os.environ.get('OPENWEATHER_API_KEY', '292d22760dfa4b5dd0dc99af0d69adf0')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()

    if not city:
        return jsonify({'error': 'City name is required'}), 400

    if len(city) < 2:
        return jsonify({'error': 'City name too short'}), 400

    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params, timeout=5)

        if response.status_code == 404:
            return jsonify({'error': 'City not found'}), 404

        if response.status_code == 401:
            return jsonify({'error': 'Invalid API key'}), 401

        if response.status_code != 200:
            return jsonify({'error': 'Weather service unavailable'}), 503

        data = response.json()

        weather = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'condition': data['weather'][0]['main']
        }

        return jsonify(weather), 200

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection error'}), 503
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
