# -*- coding: utf-8 -*-
import os

import pygame
import pyttsx3
import speech_recognition as sr
from gtts import gTTS


recognizer = sr.Recognizer()
engine = None


def _get_engine():
    global engine
    if engine is None:
        engine = pyttsx3.init()
    return engine


def speak_old(text):
    try:
        text_to_speech = _get_engine()
        text_to_speech.say(text)
        text_to_speech.runAndWait()
    except Exception:
        print(text)


def speak(text):
    temp_audio = "temp.mp3"
    try:
        tts = gTTS(text)
        tts.save(temp_audio)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception:
        print(text)
        speak_old(text)
    finally:
        try:
            pygame.mixer.music.unload()
        except Exception:
            pass
        if os.path.exists(temp_audio):
            os.remove(temp_audio)


def recognize_command_audio(recognizer_instance, audio):
    try:
        return recognizer_instance.recognize_google(audio)
    except sr.UnknownValueError:
        return recognizer_instance.recognize_google(audio, language="bn-BD")
