# -*- coding: utf-8 -*-
import os


DEFAULT_WEATHER_CITY = os.getenv("WEATHER_CITY", "Dhaka")
WEATHER_COUNTRY = os.getenv("WEATHER_COUNTRY", "Bangladesh")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NOTES_FILE = os.getenv("JARVIS_NOTES_FILE", "notes.txt")
MEMORY_FILE = os.getenv("JARVIS_MEMORY_FILE", "memory.json")
HISTORY_FILE = os.getenv("JARVIS_HISTORY_FILE", "command_history.json")
ROUTINES_FILE = os.getenv("JARVIS_ROUTINES_FILE", "routines.json")
CONVERSATION_COMMANDS = int(os.getenv("JARVIS_CONVERSATION_COMMANDS", "5"))
