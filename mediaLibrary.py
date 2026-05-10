from difflib import get_close_matches
from urllib.parse import quote_plus


favorite_media = {
    # Bangla / Bangladesh songs
    "chaad": "Tanzil Misbah Chaad Bodone",
    "ura": "Pritom Hasan Lage Ura Dhura",
    "sojoni": "Samz Vai Aay Sojoni",
    "konna": "Imran Mahmudul Konna Jinn 3",
    "churi": "Luipa Churi Cham Cham Tanvir Ahmed",
    "boishakh": "Asif Akbar Esho Hey Boishakh",
    "mayate": "Tor Mayate Bondhi Ami Bangla Romantic Song",
    "fire": "Imran Fire Ashona",
    "bolte": "Imran Bolte Bolte Cholte Cholte",
    "ami": "Imran Mahmudul Ami Nei Amate Bristy",
    "shunno": "Tanveer Evan Shunno Memories Are Forever",
    "jala": "Runa Laila Jala Jala Prince",
    "jabo": "Ishaan Mozumder Jabo Jabo Mon",
    "deora": "Coke Studio Bangla Deora",
    "kotha": "Coke Studio Bangla Kotha Koiyo Na",
    "nithur": "Ishaan Mozumder Nithur Monohor",
    "darale": "Ishaan Mozumder Darale Duare",
    "gulbahar": "Ishaan Mozumder Gulbahar",
    "chad": "Pritom Hasan Chad Mama",
    "medam": "Leyakat Ali Medam Nacere Nace Niloy Khan Sagor",

    # Hindi / India songs
    "shararat": "Shashwat Sachdev Shararat Dhurandhar",
    "bairan": "Banjaare Bairan",
    "jaiye": "Shashwat Sachdev Jaiye Sajana",
    "gehra": "Shashwat Sachdev Gehra Hua Dhurandhar",
    "sheesha": "Mitta Ror Sheesha Aakhya Mai Aakh Ghali Jo Bairan",
    "bairi": "Virat Bairi Pradeep Solanki Heena",
    "jaan": "Khan Saab Jaan Se Guzarte Hain",
    "lutt": "Shashwat Sachdev Lutt Le Gaya",
    "fortuner": "Raj Mawar Fortuner Ruchika Jangid",
    "pal": "Afusic Pal Pal",
    "sitaare": "Arijit Singh Sitaare Ikkis",
    "bangles": "Sanju Rathod Bangles",
    "majboor": "Sheheryar Rehan Majboor",
    "mithe": "Masoom Sharma Mithe Tere Bol Pari",
    "aaya": "Anirudh Ravichander Aaya Sher",
    "chadar": "Shobi Sarwan Teri Yaadon Ki Chadar Odhe",
    "saiyaara": "Tanishk Bagchi Saiyaara",
    "raat": "Madhubanti Bagchi Aaj Ki Raat",
    "humnava": "Jubin Nautiyal Humnava Mere",
    "tum": "Jubin Nautiyal Tum Hi Aana",

    # Global songs
    "golden": "HUNTRX Golden KPop Demon Hunters",
    "pinky": "KATSEYE PINKY UP",
    "ordinary": "Alex Warren Ordinary",
    "babydoll": "Dominic Fike Babydoll",
    "dracula": "Tame Impala JENNIE Dracula Remix",
    "risk": "Bruno Mars Risk It All",
    "swim": "BTS SWIM",
    "two": "BTS 2.0 Official MV",
    "madwoman": "Laufey Madwoman",
    "stateside": "PinkPantheress Zara Larsson Stateside",
}

media_categories = {
    "music": {
        "bangla song": "bangla song",
        "hindi song": "hindi song",
        "english song": "english song",
        "islamic song": "islamic song",
        "lofi song": "lofi music",
        "sad song": "sad song",
        "romantic song": "romantic song",
        "rap song": "rap song",
        "folk song": "folk song",
        "band song": "band song",
    },
    "movie": {
        "bangla movie": "bangla full movie",
        "hindi movie": "hindi full movie",
        "english movie": "english movie trailer",
        "south movie": "south indian movie",
        "korean movie": "korean movie",
        "action movie": "action movie",
        "comedy movie": "comedy movie",
        "horror movie": "horror movie",
        "romantic movie": "romantic movie",
        "animation movie": "animation movie",
    },
    "natok": {
        "bangla natok": "bangla natok",
        "eid natok": "eid natok",
        "comedy natok": "comedy natok",
        "romantic natok": "romantic natok",
        "family natok": "family natok",
        "short film": "bangla short film",
        "web series": "web series",
        "telefilm": "bangla telefilm",
        "drama serial": "drama serial",
        "korean drama": "korean drama",
    },
    "education": {
        "python tutorial": "python tutorial playlist",
        "web development": "web development tutorial playlist",
        "c programming": "c programming tutorial playlist",
        "java tutorial": "java tutorial playlist",
        "english speaking": "english speaking course",
        "math class": "math class lecture",
        "physics class": "physics class lecture",
        "chemistry class": "chemistry class lecture",
        "ielts": "ielts preparation playlist",
        "hsc lecture": "hsc lecture playlist",
    },
    "religious": {
        "quran": "quran recitation",
        "islamic lecture": "islamic lecture bangla",
        "waz": "bangla waz",
        "hamd naat": "hamd naat",
        "nasheed": "nasheed",
        "tafsir": "tafsir bangla",
        "hadith": "hadith lecture",
        "islamic history": "islamic history",
        "dua": "dua",
        "azan": "azan",
    },
    "information": {
        "bangla news": "bangla news latest",
        "international news": "international news latest",
        "sports news": "sports news latest",
        "tech news": "tech news latest",
        "business news": "business news latest",
        "weather update": "weather update",
        "documentary": "documentary",
        "science video": "science video",
        "history video": "history video",
        "biography": "biography",
    },
    "entertainment": {
        "funny video": "funny video",
        "vlog": "vlog",
        "podcast": "podcast",
        "stand up comedy": "stand up comedy",
        "gaming video": "gaming video",
        "football highlights": "football highlights",
        "cricket highlights": "cricket highlights",
        "travel video": "travel video",
        "food review": "food review",
        "tech review": "tech review",
    },
}

media_keywords = {}
for category in media_categories.values():
    media_keywords.update(category)


def youtube_search_url(query):
    return f"https://www.youtube.com/results?search_query={quote_plus(query)}"


def clean_media_command(command):
    command = command.lower().strip()
    prefixes = [
        "search youtube", "youtube search", "play", "watch", "show", "open", "search", "youtube", "play me",
        "play a", "play an", "watch a", "watch an"
    ]

    for prefix in sorted(prefixes, key=len, reverse=True):
        if command == prefix:
            return ""
        if command.startswith(prefix + " "):
            command = command.replace(prefix + " ", "", 1).strip()
            break

    remove_words = ["please", "video", "on youtube", "from youtube"]
    for word in remove_words:
        command = command.replace(word, "").strip()

    return " ".join(command.split())


def find_favorite_query(query):
    if query in favorite_media:
        return favorite_media[query], query

    matches = get_close_matches(query, favorite_media.keys(), n=1, cutoff=0.72)
    if matches:
        match = matches[0]
        return favorite_media[match], match

    return None, None


def find_category_query(query):
    if query in media_keywords:
        return media_keywords[query], query

    for keyword in sorted(media_keywords, key=len, reverse=True):
        if keyword in query:
            return query.replace(keyword, media_keywords[keyword]), keyword

    matches = get_close_matches(query, media_keywords.keys(), n=1, cutoff=0.78)
    if matches:
        match = matches[0]
        return media_keywords[match], match

    return None, None


def get_media_url(command):
    query = clean_media_command(command)
    if not query:
        return None, None
    if query == "song":
        query = "bangla song"

    favorite_query, matched_name = find_favorite_query(query)
    if favorite_query:
        return youtube_search_url(favorite_query), matched_name

    category_query, matched_name = find_category_query(query)
    if category_query:
        return youtube_search_url(category_query), matched_name

    return youtube_search_url(query), query
