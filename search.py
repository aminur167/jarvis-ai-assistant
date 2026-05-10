# -*- coding: utf-8 -*-
import webbrowser
from urllib.parse import quote_plus


SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q={query}",
    "youtube": "https://www.youtube.com/results?search_query={query}",
    "wikipedia": "https://en.wikipedia.org/wiki/Special:Search?search={query}",
    "google maps": "https://www.google.com/maps/search/{query}",
    "maps": "https://www.google.com/maps/search/{query}",
    "github": "https://github.com/search?q={query}",
    "stackoverflow": "https://stackoverflow.com/search?q={query}",
    "stack overflow": "https://stackoverflow.com/search?q={query}",
    "reddit": "https://www.reddit.com/search/?q={query}",
    "translate": "https://translate.google.com/?sl=auto&tl=en&text={query}&op=translate",
}


def clean_search_query(query):
    remove_words = ["please", "koro", "koren", "dao", "dekhaw"]
    for word in remove_words:
        query = query.replace(word, "").strip()
    return " ".join(query.split())


def get_search_request(command):
    command = command.lower().strip()
    if not command.startswith("search "):
        return None, None

    search_text = command.replace("search ", "", 1).strip()
    if not search_text:
        return None, ""

    for engine in sorted(SEARCH_ENGINES, key=len, reverse=True):
        if search_text.startswith(engine + " "):
            query = clean_search_query(search_text.replace(engine + " ", "", 1))
            return engine, query
        if search_text.endswith(" on " + engine):
            query = clean_search_query(search_text.rsplit(" on " + engine, 1)[0])
            return engine, query

    return "google", clean_search_query(search_text)


def search_web(command):
    engine, query = get_search_request(command)
    if engine is None:
        return False, None
    if not query:
        return True, "What should I search?"

    url = SEARCH_ENGINES[engine].format(query=quote_plus(query))
    webbrowser.open(url)
    return True, f"Searching {engine} for {query}"
