# -*- coding: utf-8 -*-
import os

import pygame
import pyttsx3
import speech_recognition as sr
from gtts import gTTS


recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


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
