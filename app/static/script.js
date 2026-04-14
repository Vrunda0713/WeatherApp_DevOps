const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const weatherCard = document.getElementById('weatherCard');
const errorMsg = document.getElementById('errorMsg');
const loader = document.getElementById('loader');
const hint = document.getElementById('hint');

function showLoader() {
  loader.classList.remove('hidden');
  weatherCard.classList.add('hidden');
  errorMsg.classList.add('hidden');
  hint.classList.add('hidden');
}

function showError(msg) {
  loader.classList.add('hidden');
  weatherCard.classList.add('hidden');
  errorMsg.textContent = msg;
  errorMsg.classList.remove('hidden');
}

function showWeather(data) {
  loader.classList.add('hidden');
  errorMsg.classList.add('hidden');

  document.getElementById('cityName').textContent = data.city;
  document.getElementById('countryBadge').textContent = data.country;
  document.getElementById('temperature').textContent = data.temperature;
  document.getElementById('feelsLike').textContent = data.feels_like;
  document.getElementById('humidity').textContent = data.humidity;
  document.getElementById('windSpeed').textContent = data.wind_speed;
  document.getElementById('condition').textContent = data.description;
  document.getElementById('weatherIcon').src =
    `https://openweathermap.org/img/wn/${data.icon}@2x.png`;

  weatherCard.classList.remove('hidden');
}

async function fetchWeather() {
  const city = cityInput.value.trim();
  if (!city) return;

  showLoader();

  try {
    const res = await fetch(`/weather?city=${encodeURIComponent(city)}`);
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || 'Something went wrong.');
    } else {
      showWeather(data);
    }
  } catch (err) {
    showError('Network error. Please try again.');
  }
}

searchBtn.addEventListener('click', fetchWeather);
cityInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') fetchWeather();
});
