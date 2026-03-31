import os

import requests


def _suggestions_from_weather(temp_c: float, humidity: int) -> list[str]:
    suggestions = []

    if temp_c >= 35:
        suggestions.append("High heat alert: prefer early morning/evening irrigation.")
    elif temp_c <= 15:
        suggestions.append("Cool conditions: avoid overwatering and monitor fungal growth.")
    else:
        suggestions.append("Temperature is moderate: maintain regular crop monitoring.")

    if humidity >= 80:
        suggestions.append("High humidity: improve ventilation and check for fungal diseases.")
    elif humidity <= 35:
        suggestions.append("Low humidity: consider mulching to conserve soil moisture.")
    else:
        suggestions.append("Humidity is manageable: continue balanced watering schedule.")

    suggestions.append("Follow local agri advisories for crop-specific nutrient sprays.")
    return suggestions


def _demo_weather(city: str) -> dict:
    temp_c = 29.0
    humidity = 62
    return {
        "city": city.title(),
        "temperature_c": temp_c,
        "humidity": humidity,
        "condition": "Partly Cloudy (Demo)",
        "suggestions": _suggestions_from_weather(temp_c, humidity),
        "note": "Demo weather shown. Add WEATHER_API_KEY in .env or check network access for live data.",
    }


def fetch_weather_data(city: str) -> dict:
    """
    Fetch weather info from OpenWeatherMap and produce farming suggestions.
    If API key is missing or the request fails, return demo weather data.
    """
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return _demo_weather(city)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()

        temp_c = float(payload["main"]["temp"])
        humidity = int(payload["main"]["humidity"])
        condition = payload["weather"][0]["description"].title()
        city_name = payload.get("name", city).title()

        return {
            "city": city_name,
            "temperature_c": temp_c,
            "humidity": humidity,
            "condition": condition,
            "suggestions": _suggestions_from_weather(temp_c, humidity),
        }
    except requests.RequestException:
        return _demo_weather(city)
    except (KeyError, ValueError, TypeError):
        return _demo_weather(city)
