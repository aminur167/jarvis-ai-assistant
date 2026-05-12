# Jarvis AI Assistant

A modular Python voice assistant with wake-word listening, desktop GUI control, Bangla/Banglish command support, productivity tools, system utilities, web search, weather, news, and AI-powered fallback responses.

Jarvis is designed as a practical desktop assistant: it can listen for the `Jarvis` wake word, continue a short conversation, execute common commands, remember useful information, manage tasks and routines, and provide a simple GUI for text or microphone-based interaction.

## Highlights

- Voice assistant with wake-word activation and follow-up conversation mode
- Desktop GUI for typing commands, using the microphone, and quick actions
- Bangla and Banglish command normalization for more natural usage
- Persistent notes, memory, command history, tasks, and custom routines
- Weather, news, web search, YouTube/media search, and website shortcuts
- App launcher, folder opener, clipboard tools, calculator, and currency conversion
- System controls for volume, mute, battery status, screenshots, shutdown, and restart
- Daily briefing with date, time, weather, and news
- OpenAI fallback for general questions and explanations
- Clean module-based architecture for adding new commands easily

## Tech Stack

- Python
- Tkinter for the desktop GUI
- SpeechRecognition for speech input
- gTTS, pygame, and pyttsx3 for speech output
- OpenAI API for AI fallback responses
- Open-Meteo / wttr.in for weather
- NewsAPI for headlines
- JSON files for lightweight local persistence

## Project Preview

Jarvis supports both voice-first and GUI-first workflows.

```text
User: Jarvis
Jarvis: Ya
User: daily briefing
Jarvis: Today is Tuesday, May 12, 2026. The current time is 11:20 PM...
```

```text
User: create routine study mode: open vs code; play focus music; set timer for 25 minutes
Jarvis: Saved routine study mode with 3 commands.
```

```text
User: add task finish portfolio project
Jarvis: Task 1 added: finish portfolio project.
```

## Features

### Voice And GUI

- Wake word: `Jarvis`
- Follow-up conversation mode after activation
- Text command input through GUI
- Microphone command input through GUI
- Quick GUI buttons for briefing, routines, tasks, and notes

### Productivity

- Notes: create, show, and clear notes
- Tasks: add, show, complete, reopen, delete, and clear tasks
- Reminders and timers
- Persistent user memory
- Command history
- Custom routines for running multiple commands from one shortcut

### Information

- Current time and date
- Weather lookup by city
- Daily briefing
- News headlines
- Web search
- YouTube/media search
- Wikipedia search

### Desktop Utilities

- Open common websites
- Open local apps such as Notepad, Calculator, Chrome, Edge, VS Code, and PowerShell
- Open common folders such as Desktop, Downloads, Documents, and Pictures
- Clipboard read, copy, and clear
- Calculator and currency converter
- Volume, mute, battery, screenshot, shutdown, and restart commands

### AI Assistant

- Ask short or long questions
- AI fallback for commands that are not handled by local modules
- Optional OpenAI API integration through environment variables

## Installation

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd jarvis-ai-assistant
pip install -r requirements.txt
```

For microphone support on Windows, PyAudio may require an additional install step:

```bash
pip install pipwin
pipwin install pyaudio
```

## Configuration

Most features work without API keys. AI fallback and news require optional environment variables.

| Variable | Purpose | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | Enables AI fallback responses | Not set |
| `NEWS_API_KEY` | Enables news headlines | Not set |
| `WEATHER_CITY` | Default city for weather and briefing | `Dhaka` |
| `WEATHER_COUNTRY` | Default country for location lookup | `Bangladesh` |
| `JARVIS_CONVERSATION_COMMANDS` | Number of follow-up commands after wake word | `5` |
| `JARVIS_NOTES_FILE` | Notes storage file | `notes.txt` |
| `JARVIS_MEMORY_FILE` | Memory storage file | `memory.json` |
| `JARVIS_HISTORY_FILE` | Command history storage file | `command_history.json` |
| `JARVIS_ROUTINES_FILE` | Routines storage file | `routines.json` |
| `JARVIS_TASKS_FILE` | Tasks storage file | `tasks.json` |

Windows example:

```bash
set OPENAI_API_KEY=your_openai_key
set NEWS_API_KEY=your_newsapi_key
set WEATHER_CITY=Dhaka
```

## Usage

Run the voice assistant:

```bash
python main.py
```

Say `Jarvis`, then give a command. After the wake word, Jarvis stays active for a short conversation. Say `stop`, `sleep`, or `thank you` to return to sleep mode.

Run the desktop GUI:

```bash
python gui.py
```

## Example Commands

| Category | Commands |
| --- | --- |
| Briefing | `daily briefing`, `morning briefing`, `start my day` |
| Tasks | `add task finish assignment`, `show tasks`, `complete task 1`, `reopen task 1` |
| Routines | `create routine study mode: open vs code; play focus music`, `run routine study mode` |
| Notes | `take note finish Python project`, `show notes`, `clear notes` |
| Memory | `remember my college name is ABC College`, `what is my college name` |
| Reminders | `set timer for 10 minutes`, `remind me to study at 8 pm` |
| Search | `search python tutorial`, `search youtube bangla natok`, `search wikipedia Bangladesh` |
| Weather | `weather in Dhaka`, `dhaka er abohawa bolo` |
| Apps | `open calculator`, `open notepad`, `open chrome`, `open vs code` |
| System | `volume up`, `mute`, `battery status`, `take screenshot` |
| AI | `ask jarvis explain recursion`, `short answer what is AI`, `long answer explain machine learning` |

## Project Structure

```text
jarvis-ai-assistant/
|-- main.py              # Voice assistant loop and command router
|-- gui.py               # Desktop GUI for text and microphone commands
|-- speech.py            # Speech recognition and text-to-speech helpers
|-- banglaCommands.py    # Bangla/Banglish command normalization
|-- ai_service.py        # OpenAI fallback responses
|-- briefing.py          # Daily briefing
|-- tasks.py             # Persistent task manager
|-- routines.py          # Custom multi-command routines
|-- notes.py             # Local notes
|-- memory.py            # Persistent user memory
|-- history.py           # Command history
|-- reminders.py         # Timers and reminders
|-- weather.py           # Weather lookup
|-- news.py              # News headlines
|-- search.py            # Web, YouTube, and Wikipedia search
|-- mediaLibrary.py      # Media and YouTube helpers
|-- websites.py          # Website shortcuts
|-- apps.py              # Local app launcher
|-- file_opener.py       # Common folder opener
|-- clipboard_helper.py  # Clipboard tools
|-- calculator.py        # Calculator and currency converter
|-- system_control.py    # System utilities
|-- config.py            # Environment-based configuration
`-- requirements.txt     # Python dependencies
```

## Architecture

The assistant uses a simple command-handler pipeline. Each feature module exposes a handler function that receives a command and returns whether it handled the command plus a response.

```python
def handle_feature(command):
    if not matching_command:
        return False, None
    return True, "Response for the user"
```

This keeps the project easy to extend. New features can be added as separate modules and registered in `COMMAND_HANDLERS` inside `main.py`.

## Data Storage

Jarvis stores lightweight local data in plain files:

- `notes.txt` for notes
- `memory.json` for remembered user facts
- `command_history.json` for recent commands
- `routines.json` for custom routines
- `tasks.json` for task management

These files are local to the user and can be customized with environment variables.

## Roadmap

- Improve GUI with tabs for tasks, notes, routines, and settings
- Add a persistent settings screen
- Add unit tests for command handlers
- Add plugin-style command loading
- Add export/import for notes, tasks, memory, and routines
- Improve Bangla voice output and command coverage

## Why This Project

This project demonstrates practical Python application development with speech recognition, GUI design, API integration, local persistence, command routing, and modular architecture. It is built to be useful as a real desktop assistant while remaining easy to read, maintain, and extend.
