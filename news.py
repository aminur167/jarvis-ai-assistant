# -*- coding: utf-8 -*-
import requests

from config import NEWS_API_KEY


def get_news_headlines(country="in", limit=5):
    if not NEWS_API_KEY:
        return "News API key is missing. Please set NEWS_API_KEY first."

    try:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWS_API_KEY}",
            timeout=10,
        )
        if response.status_code != 200:
            return "Sorry, I could not get the news right now."

        articles = response.json().get("articles", [])
        titles = [article.get("title") for article in articles[:limit] if article.get("title")]
        if not titles:
            return "Sorry, I did not find any news right now."
        return titles
    except Exception:
        return "Sorry, I could not get the news right now."
