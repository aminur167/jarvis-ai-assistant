# -*- coding: utf-8 -*-
from search import SEARCH_ENGINES


BANGLA_WORD_ALIASES = {
    "গুগল": "google",
    "ইউটিউব": "youtube",
    "ফেসবুক": "facebook",
    "ইনস্টাগ্রাম": "instagram",
    "জিমেইল": "gmail",
    "গিটহাব": "github",
    "চ্যাটজিপিটি": "chatgpt",
    "উইকিপিডিয়া": "wikipedia",
    "উইকিপিডিয়া": "wikipedia",
    "ম্যাপ": "maps",
    "ম্যাপস": "maps",
    "গান": "song",
    "নাটক": "natok",
    "মুভি": "movie",
    "সিনেমা": "movie",
    "ওয়াজ": "waz",
    "ওয়াজ": "waz",
    "ঢাকা": "dhaka",
    "ঢাকার": "dhaka",
    "বগুড়া": "bogura",
    "বগুড়া": "bogura",
    "চট্টগ্রাম": "chittagong",
    "সিলেট": "sylhet",
    "রাজশাহী": "rajshahi",
    "রংপুর": "rangpur",
    "খুলনা": "khulna",
    "বরিশাল": "barishal",
    "ময়মনসিংহ": "mymensingh",
    "ময়মনসিংহ": "mymensingh",
}


def strip_command_words(text, words):
    for word in sorted(words, key=len, reverse=True):
        text = text.replace(word, " ")
    return " ".join(text.split())


def replace_bangla_aliases(command):
    for bangla, english in sorted(BANGLA_WORD_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        command = command.replace(bangla, english)
    return command


def normalize_bangla_banglish_command(command):
    command = command.lower().strip()
    command = command.replace("?", "").replace("।", "").replace(",", " ")
    command = replace_bangla_aliases(command)
    command = " ".join(command.split())

    open_words = [
        "khulo", "khol", "open koro", "open kore dao", "চালু করো",
        "খুলো", "ওপেন করো", "ওপেন করে দাও",
    ]
    play_words = [
        "chalao", "chaliye dao", "play koro", "dekhao", "দেখাও",
        "চালাও", "চালিয়ে দাও", "প্লে করো",
    ]
    search_words = [
        "search koro", "search kore dao", "khujo", "khuj", "সার্চ করো",
        "সার্চ করে দাও", "খুঁজো", "খুজো",
    ]
    time_words = [
        "somoy", "shomoy", "time bolo", "somoy bolo", "কয়টা বাজে",
        "কয়টা বাজে", "সময়", "সময়", "সময় বলো",
    ]
    date_words = [
        "tarikh", "date bolo", "ajker date", "aj ki bar", "তারিখ",
        "আজকের তারিখ", "আজ কী বার", "আজ কি বার",
    ]
    weather_words = [
        "abohawa", "abohawa bolo", "weather bolo", "tapmatra",
        "আবহাওয়া", "আবহাওয়া", "তাপমাত্রা",
    ]
    news_words = ["khobor", "news bolo", "খবর", "নিউজ"]
    note_words = ["note rakho", "note koro", "নোট রাখো", "নোট করো"]
    remember_words = ["mone rakho", "remember koro", "মনে রাখো"]
    ask_words = ["jarvis ke jiggesh koro", "jiggesh koro", "জিজ্ঞেস করো", "জারভিসকে জিজ্ঞেস করো"]
    media_words = [
        "gaan", "gan", "song", "natok", "movie", "cinema", "waz",
        "lecture", "tutorial", "গান", "নাটক", "মুভি", "সিনেমা", "ওয়াজ", "ওয়াজ",
    ]

    if any(word in command for word in time_words):
        return "time"
    if any(word in command for word in date_words):
        return "date"
    if any(word in command for word in news_words):
        return "news"
    if command.startswith("amar nam "):
        return "my name is " + command.replace("amar nam ", "", 1).strip()
    if command.startswith("আমার নাম "):
        return "my name is " + command.replace("আমার নাম ", "", 1).strip()
    if command in ("ami last ki bolsilam", "last command bolo", "আমি শেষ কি বলেছিলাম"):
        return "last command"

    for word in note_words:
        if command.startswith(word + " "):
            note = command.replace(word + " ", "", 1).strip()
            return f"take note {note}"

    for word in remember_words:
        if command.startswith(word + " "):
            fact = command.replace(word + " ", "", 1).strip()
            return f"remember {fact}"

    for word in ask_words:
        if command.startswith(word + " "):
            prompt = command.replace(word + " ", "", 1).strip()
            return f"ask jarvis {prompt}"

    if any(word in command for word in weather_words):
        location = strip_command_words(command, weather_words + ["er", "e", "এর", "এ", "bolo", "bolen", "বল", "বলো"])
        if location:
            return f"weather in {location}"
        return "weather"

    for engine in sorted(SEARCH_ENGINES, key=len, reverse=True):
        engine_markers = [f"{engine} e", f"{engine} a", f"{engine} এ"]
        if any(marker in command for marker in engine_markers) and any(word in command for word in search_words):
            query = strip_command_words(command, search_words + engine_markers + ["এ"])
            return f"search {engine} {query}".strip()

    if any(word in command for word in search_words):
        query = strip_command_words(command, search_words)
        return f"search {query}".strip()

    if any(word in command for word in play_words) and any(word in command for word in media_words):
        query = strip_command_words(command, play_words)
        query = query.replace("gaan", "song").replace("gan", "song").replace("গান", "song")
        query = query.replace("নাটক", "natok").replace("মুভি", "movie").replace("সিনেমা", "movie")
        query = query.replace("ওয়াজ", "waz").replace("ওয়াজ", "waz")
        return f"play {query}".strip()

    for word in open_words:
        if command.endswith(" " + word):
            site_name = command.rsplit(" " + word, 1)[0].strip()
            return f"open {site_name}"
        if command.startswith(word + " "):
            site_name = command.replace(word + " ", "", 1).strip()
            return f"open {site_name}"

    return command
