# -*- coding: utf-8 -*-
import threading
import tkinter as tk
from tkinter import ttk

import speech_recognition as sr

from main import process_command_text
from speech import recognize_command_audio


class JarvisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jarvis AI Assistant")
        self.geometry("760x560")
        self.minsize(640, 460)
        self.configure(bg="#f4f6f8")

        self.speak_enabled = tk.BooleanVar(value=True)
        self.status_text = tk.StringVar(value="Ready")
        self.command_text = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        header = ttk.Frame(root)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.columnconfigure(0, weight=1)

        title = ttk.Label(header, text="Jarvis AI Assistant", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, sticky="w")

        status = ttk.Label(header, textvariable=self.status_text)
        status.grid(row=0, column=1, sticky="e")

        self.log = tk.Text(root, wrap=tk.WORD, height=18, borderwidth=1, relief=tk.SOLID)
        self.log.grid(row=1, column=0, sticky="nsew")
        self.log.configure(state=tk.DISABLED, font=("Segoe UI", 10), padx=10, pady=10)

        controls = ttk.Frame(root)
        controls.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        controls.columnconfigure(0, weight=1)

        entry = ttk.Entry(controls, textvariable=self.command_text, font=("Segoe UI", 11))
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        entry.bind("<Return>", lambda _event: self.submit_text_command())
        entry.focus_set()

        send_button = ttk.Button(controls, text="Send", command=self.submit_text_command)
        send_button.grid(row=0, column=1, padx=(0, 8))

        mic_button = ttk.Button(controls, text="Mic", command=self.submit_voice_command)
        mic_button.grid(row=0, column=2, padx=(0, 8))

        speak_toggle = ttk.Checkbutton(controls, text="Speak", variable=self.speak_enabled)
        speak_toggle.grid(row=0, column=3)

        quick = ttk.Frame(root)
        quick.grid(row=3, column=0, sticky="ew", pady=(10, 0))

        ttk.Button(quick, text="Daily Briefing", command=lambda: self.run_command("daily briefing")).pack(side=tk.LEFT)
        ttk.Button(quick, text="Show Routines", command=lambda: self.run_command("show routines")).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        ttk.Button(quick, text="Show Tasks", command=lambda: self.run_command("show tasks")).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(quick, text="Show Notes", command=lambda: self.run_command("show notes")).pack(side=tk.LEFT, padx=(8, 0))

    def append_log(self, speaker, text):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, f"{speaker}: {text}\n")
        self.log.see(tk.END)
        self.log.configure(state=tk.DISABLED)

    def set_status(self, text):
        self.status_text.set(text)

    def submit_text_command(self):
        command = self.command_text.get().strip()
        if not command:
            return
        self.command_text.set("")
        self.run_command(command)

    def submit_voice_command(self):
        thread = threading.Thread(target=self._listen_once, daemon=True)
        thread.start()

    def _listen_once(self):
        self.after(0, self.set_status, "Listening...")
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognize_command_audio(recognizer, audio)
            self.after(0, self.run_command, command)
        except sr.WaitTimeoutError:
            self.after(0, self.append_log, "Jarvis", "I did not hear anything.")
        except sr.UnknownValueError:
            self.after(0, self.append_log, "Jarvis", "Sorry, I could not understand that.")
        except sr.RequestError:
            self.after(0, self.append_log, "Jarvis", "Speech recognition service is unavailable.")
        except Exception as error:
            self.after(0, self.append_log, "Jarvis", f"Microphone error: {error}")
        finally:
            self.after(0, self.set_status, "Ready")

    def run_command(self, command):
        self.append_log("You", command)
        self.set_status("Working...")
        thread = threading.Thread(target=self._process_command, args=(command,), daemon=True)
        thread.start()

    def _process_command(self, command):
        responses = process_command_text(command, speak_response=self.speak_enabled.get())
        if not responses:
            responses = ["Done."]
        for response in responses:
            self.after(0, self.append_log, "Jarvis", response)
        self.after(0, self.set_status, "Ready")


if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()
