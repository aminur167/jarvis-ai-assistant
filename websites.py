# -*- coding: utf-8 -*-
import webbrowser


WEBSITE_CATEGORIES = {
    "social": {
        "facebook": "https://facebook.com",
        "instagram": "https://instagram.com",
        "x": "https://x.com",
        "youtube": "https://youtube.com",
        "linkedin": "https://linkedin.com",
        "reddit": "https://reddit.com",
        "pinterest": "https://pinterest.com",
        "tiktok": "https://tiktok.com",
        "snapchat": "https://web.snapchat.com",
        "threads": "https://threads.net",
    },
    "google": {
        "google": "https://google.com",
        "gmail": "https://mail.google.com",
        "drive": "https://drive.google.com",
        "calendar": "https://calendar.google.com",
        "maps": "https://maps.google.com",
        "translate": "https://translate.google.com",
        "photos": "https://photos.google.com",
        "docs": "https://docs.google.com",
        "sheets": "https://sheets.google.com",
        "meet": "https://meet.google.com",
    },
    "study": {
        "wikipedia": "https://wikipedia.org",
        "w3schools": "https://w3schools.com",
        "geeksforgeeks": "https://geeksforgeeks.org",
        "khan academy": "https://khanacademy.org",
        "coursera": "https://coursera.org",
        "udemy": "https://udemy.com",
        "edx": "https://edx.org",
        "duolingo": "https://duolingo.com",
        "quora": "https://quora.com",
        "medium": "https://medium.com",
    },
    "coding": {
        "github": "https://github.com",
        "stack overflow": "https://stackoverflow.com",
        "leetcode": "https://leetcode.com",
        "codeforces": "https://codeforces.com",
        "codechef": "https://codechef.com",
        "hackerrank": "https://hackerrank.com",
        "gitlab": "https://gitlab.com",
        "replit": "https://replit.com",
        "npm": "https://npmjs.com",
        "python": "https://python.org",
    },
    "ai": {
        "chatgpt": "https://chatgpt.com",
        "claude": "https://claude.ai",
        "gemini": "https://gemini.google.com",
        "openai": "https://openai.com",
        "ai studio": "https://aistudio.google.com",
        "perplexity": "https://perplexity.ai",
        "copilot": "https://copilot.microsoft.com",
        "hugging face": "https://huggingface.co",
        "poe": "https://poe.com",
        "blackbox": "https://blackbox.ai",
    },
}

WEBSITES = {}
for category in WEBSITE_CATEGORIES.values():
    WEBSITES.update(category)

WEBSITE_ALIASES = {
    "twitter": "x",
    "stackoverflow": "stack overflow",
    "google ai studio": "ai studio",
    "google map": "maps",
    "google maps": "maps",
    "google doc": "docs",
    "google docs": "docs",
    "google sheet": "sheets",
    "google sheets": "sheets",
    "google meet": "meet",
}


def open_url(url):
    webbrowser.open(url)


def get_website_name(command):
    command = command.lower().strip()
    if not command.startswith("open "):
        return None

    site_name = command.replace("open ", "", 1).strip()
    site_name = site_name.replace("website", "").replace("site", "").strip()
    return WEBSITE_ALIASES.get(site_name, site_name)


def open_website(command):
    site_name = get_website_name(command)
    if not site_name:
        return False, None

    if site_name in WEBSITES:
        open_url(WEBSITES[site_name])
        return True, f"Opening {site_name}"

    for name in sorted(WEBSITES, key=len, reverse=True):
        if name in site_name:
            open_url(WEBSITES[name])
            return True, f"Opening {name}"

    return True, "Sorry, I do not know this website yet."
