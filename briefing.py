# -*- coding: utf-8 -*-
from datetime import datetime

from config import DEFAULT_WEATHER_CITY
from news import get_news_headlines
from weather import tell_weather


def _format_news():
    headlines = get_news_headlines(limit=3)
    if isinstance(headlines, list):
        return "Top news: " + " ".join(f"{index}. {title}." for index, title in enumerate(headlines, 1))
    if "api key is missing" in headlines.lower():
        return "News is not configured yet."
    return headlines


def get_daily_briefing():
    now = datetime.now()
    parts = [
        f"Good day. Today is {now.strftime('%A, %B %d, %Y')}.",
        f"The current time is {now.strftime('%I:%M %p')}.",
    ]

    handled, weather_text = tell_weather(city=DEFAULT_WEATHER_CITY, speak_error=False)
    if handled and weather_text:
        parts.append(weather_text)
    else:
        parts.append("Weather is not available right now.")

    parts.append(_format_news())
    return parts


def handle_daily_briefing(command):
    command = command.lower().strip()
    briefing_commands = (
        "daily briefing",
        "morning briefing",
        "today briefing",
        "brief me",
        "start my day",
        "ajker briefing",
        "ajker update",
    )
    if command not in briefing_commands:
        return False, None
    return True, get_daily_briefing()
