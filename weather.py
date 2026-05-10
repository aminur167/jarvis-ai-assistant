# -*- coding: utf-8 -*-
from urllib.parse import quote

import requests

from config import DEFAULT_WEATHER_CITY, WEATHER_COUNTRY


WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "foggy",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
    99: "thunderstorm with heavy hail",
}


def clean_location_name(location):
    location = location.lower().strip()
    remove_words = [
        "current", "weather", "temperature", "forecast", "in", "of", "for",
        "at", "the", "today", "now", "please", "bolo", "bolen", "dao", "dekhaw",
    ]
    words = [word for word in location.replace(",", " ").split() if word not in remove_words]
    return " ".join(words).strip()


def get_weather_city(command):
    command = command.lower().strip()
    weather_phrases = [
        "current weather in", "weather in", "weather of", "weather for",
        "current temperature in", "temperature in", "temperature of",
        "forecast in", "forecast for",
    ]

    for phrase in weather_phrases:
        if phrase in command:
            city = command.split(phrase, 1)[1].strip()
            return clean_location_name(city) or DEFAULT_WEATHER_CITY

    if command.endswith(" weather"):
        return clean_location_name(command[:-8]) or DEFAULT_WEATHER_CITY
    if command.endswith(" temperature"):
        return clean_location_name(command[:-12]) or DEFAULT_WEATHER_CITY
    if "weather" in command or "temperature" in command or "forecast" in command:
        return DEFAULT_WEATHER_CITY

    return clean_location_name(command) or DEFAULT_WEATHER_CITY


def get_weather_location(city):
    if WEATHER_COUNTRY.lower() in city.lower() or "," in city:
        return city
    return f"{city}, {WEATHER_COUNTRY}"


def format_resolved_location(location):
    parts = [
        location.get("name"),
        location.get("admin2"),
        location.get("admin1"),
        location.get("country"),
    ]
    unique_parts = []
    for part in parts:
        if part and part not in unique_parts:
            unique_parts.append(part)
    return ", ".join(unique_parts)


def geocode_location(city):
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    if response.status_code != 200:
        return None

    results = response.json().get("results", [])
    if not results and WEATHER_COUNTRY.lower() not in city.lower() and "," not in city:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": get_weather_location(city), "count": 1, "language": "en", "format": "json"},
            timeout=10,
        )
        if response.status_code == 200:
            results = response.json().get("results", [])

    if not results:
        return None
    return results[0]


def get_open_meteo_weather(city):
    location = geocode_location(city)
    if location is None:
        return None

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code",
            "timezone": "auto",
        },
        timeout=10,
    )
    if response.status_code != 200:
        return None

    current = response.json().get("current", {})
    if not current:
        return None

    return {
        "location": format_resolved_location(location),
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "humidity": current.get("relative_humidity_2m"),
        "description": WEATHER_CODES.get(current.get("weather_code"), "updated weather"),
    }


def get_wttr_weather(city):
    locations = [city]
    bangladesh_location = get_weather_location(city)
    if bangladesh_location not in locations:
        locations.append(bangladesh_location)

    response = None
    location = city
    for location in locations:
        response = requests.get(f"https://wttr.in/{quote(location)}?format=j1", timeout=10)
        if response.status_code == 200:
            break

    if response is None or response.status_code != 200:
        return None

    current_conditions = response.json().get("current_condition", [])
    if not current_conditions:
        return None

    current = current_conditions[0]
    return {
        "location": location,
        "temperature": current.get("temp_C"),
        "feels_like": current.get("FeelsLikeC"),
        "humidity": current.get("humidity"),
        "description": current.get("weatherDesc", [{}])[0].get("value", "updated weather"),
    }


def get_weather_data(city):
    return get_open_meteo_weather(city) or get_wttr_weather(city)


def tell_weather(command=None, city=None, speak_error=True):
    city = city or get_weather_city(command or "")
    if not city:
        city = DEFAULT_WEATHER_CITY

    try:
        weather = get_weather_data(city)
        if weather is None:
            if speak_error:
                return True, "Sorry, I could not get the weather right now."
            return False, None

        return True, (
            f"I found the location as {weather['location']}. Current weather is "
            f"{weather['description']}. Temperature is {weather['temperature']} degrees Celsius, "
            f"feels like {weather['feels_like']} degrees, with {weather['humidity']} percent humidity."
        )
    except Exception:
        if speak_error:
            return True, "Sorry, I could not get the weather right now."
        return False, None


def looks_like_location_command(command):
    command = command.lower().strip()
    blocked_words = [
        "open", "play", "news", "time", "date", "day", "what", "who", "why",
        "how", "tell", "write", "make", "create", "search", "google",
    ]
    words = command.split()
    return 1 <= len(words) <= 5 and not any(word in words for word in blocked_words)
