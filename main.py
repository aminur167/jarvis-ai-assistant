# -*- coding: utf-8 -*-
from datetime import datetime

import speech_recognition as sr

import mediaLibrary
from ai_service import ai_process
from apps import handle_app
from banglaCommands import normalize_bangla_banglish_command
from calculator import handle_calculator
from clipboard_helper import handle_clipboard
from config import CONVERSATION_COMMANDS
from file_opener import handle_file_opener
from history import handle_history, record_command
from memory import handle_memory
from news import get_news_headlines
from notes import handle_notes
from reminders import handle_reminder
from search import search_web
from speech import recognize_command_audio, speak
from system_control import handle_system_control
from weather import looks_like_location_command, tell_weather
from websites import open_website


def open_media(command):
    command = command.lower().strip()
    media_starters = ("play ", "watch ", "show ")
    youtube_searches = ("search youtube", "youtube search")
    media_keyword_used = any(keyword in command for keyword in mediaLibrary.media_keywords)

    if (
        not command.startswith(media_starters)
        and not any(command.startswith(item) for item in youtube_searches)
        and not (command.startswith("open ") and media_keyword_used)
    ):
        return False, None

    url, title = mediaLibrary.get_media_url(command)
    if not url:
        return True, "What should I play?"

    try:
        import webbrowser

        webbrowser.open(url)
        return True, f"Playing {title} on YouTube"
    except Exception:
        return True, "Sorry, I could not open YouTube right now."


def tell_time(command):
    if "time" not in command.lower():
        return False, None
    now = datetime.now()
    return True, f"The current time is {now.strftime('%I:%M %p')}"


def tell_date(command):
    command = command.lower()
    if "date" not in command and "day" not in command:
        return False, None
    today = datetime.now()
    return True, f"Today is {today.strftime('%A, %B %d, %Y')}"


def handle_weather(command):
    lower_command = command.lower()
    if "weather" in lower_command or "temperature" in lower_command:
        return tell_weather(command)
    return False, None


def handle_news(command):
    if "news" not in command.lower():
        return False, None
    headlines = get_news_headlines()
    if isinstance(headlines, str):
        return True, headlines
    return True, headlines


def handle_ai_command(command):
    lower_command = command.lower().strip()
    answer_mode = "short"

    if lower_command.startswith("ask jarvis "):
        prompt = command[len("ask jarvis "):].strip()
    elif lower_command.startswith("ask "):
        prompt = command[len("ask "):].strip()
    elif lower_command.startswith("long answer "):
        answer_mode = "long"
        prompt = command[len("long answer "):].strip()
    elif lower_command.startswith("short answer "):
        answer_mode = "short"
        prompt = command[len("short answer "):].strip()
    else:
        return False, None

    if not prompt:
        return True, "What should I ask?"
    return True, ai_process(prompt, answer_mode=answer_mode)


def handle_ai_fallback(command):
    return True, ai_process(command)


COMMAND_HANDLERS = [
    handle_reminder,
    handle_memory,
    handle_history,
    handle_calculator,
    handle_clipboard,
    handle_system_control,
    search_web,
    open_media,
    handle_file_opener,
    handle_app,
    open_website,
    tell_time,
    tell_date,
    handle_weather,
    handle_news,
    handle_notes,
    handle_ai_command,
]


def process_command(command):
    if not command or not command.strip():
        speak("I did not hear any command.")
        return

    original_command = command.strip()
    command = normalize_bangla_banglish_command(original_command)
    record_command(original_command, command)

    for handler in COMMAND_HANDLERS:
        handled, response = handler(command)
        if handled:
            if isinstance(response, list):
                for item in response:
                    speak(item)
            elif response:
                speak(response)
            return

    if looks_like_location_command(command):
        handled, response = tell_weather(city=command, speak_error=False)
        if handled and response:
            speak(response)
            return

    handled, response = handle_ai_fallback(command)
    if handled and response:
        speak(response)


def listen_for_followup_commands(recognizer):
    for _ in range(CONVERSATION_COMMANDS):
        try:
            with sr.Microphone() as source:
                print("Jarvis Active...")
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
                command = recognize_command_audio(recognizer, audio)

            if command.lower().strip() in ("stop", "exit", "sleep", "go to sleep", "thank you"):
                speak("Okay, going back to sleep.")
                return

            process_command(command)
            speak("Anything else?")
        except sr.WaitTimeoutError:
            speak("I did not hear anything. Going back to sleep.")
            return
        except sr.UnknownValueError:
            speak("Sorry, I could not understand that.")
        except sr.RequestError:
            speak("Sorry, speech recognition service is unavailable.")
            return

    speak("Conversation mode ended.")


def listen_for_jarvis():
    speak("Initializing Jarvis.")
    while True:
        recognizer = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Ya")
                listen_for_followup_commands(recognizer)

        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            speak("Sorry, speech recognition service is unavailable.")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    listen_for_jarvis()
