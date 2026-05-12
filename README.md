# jarvis-ai-assistant

A Python voice assistant that listens for the wake word `Jarvis` and handles web, media, search, weather, reminders, system controls, folders, clipboard, calculator, notes, local apps, memory, command history, conversation mode, news, and AI fallback commands.

## Setup

```bash
pip install -r requirements.txt
```

For microphone support on Windows, you may also need PyAudio:

```bash
pip install pipwin
pipwin install pyaudio
```

Optional environment variables:

```bash
set OPENAI_API_KEY=your_openai_key
set NEWS_API_KEY=your_newsapi_key
set WEATHER_CITY=Dhaka
set WEATHER_COUNTRY=Bangladesh
set JARVIS_CONVERSATION_COMMANDS=5
set JARVIS_ROUTINES_FILE=routines.json
```

## Run

```bash
python main.py
```

Say `Jarvis`, then give a command.

After the wake word, Jarvis stays active for a short conversation. Say `stop`, `sleep`, or `thank you` to end conversation mode.

To use the desktop interface:

```bash
python gui.py
```

## Example Commands

Websites:
- `open google`
- `open github`
- `open google maps`
- `google khulo`
- `গুগল খুলো`

Search:
- `search python tutorial`
- `search youtube bangla natok`
- `search wikipedia Bangladesh`
- `youtube e python tutorial search koro`

Media:
- `play chaad`
- `play bangla song`
- `watch python tutorial`
- `open bangla natok`
- `gaan chalao`
- `গান চালাও`

Weather:
- `weather in Dhaka`
- `Dupchanchia Bogura`
- `dhaka er abohawa bolo`
- `ঢাকার আবহাওয়া বলো`

Notes:
- `take note finish Python project`
- `show notes`
- `clear notes`

Memory:
- `my name is Aminur`
- `remember my college name is ABC College`
- `what is my name`
- `what is my college name`
- `show memory`
- `clear memory`

Command history:
- `what did I ask last`
- `last command`
- `show history`
- `clear history`

AI mode:
- `ask jarvis explain recursion`
- `ask what is coding`
- `short answer what is AI`
- `long answer explain machine learning`

Reminder and timer:
- `set timer for 10 minutes`
- `set timer for 30 seconds`
- `remind me to study at 8 pm`
- `remind me to check email in 15 minutes`

System control:
- `volume up`
- `volume down`
- `mute`
- `unmute`
- `battery status`
- `take screenshot`
- `shutdown confirm`
- `restart confirm`

Files and folders:
- `open desktop`
- `open downloads`
- `open documents`
- `open pictures`
- `open my project`

Clipboard:
- `read clipboard`
- `copy this meeting at 5 pm`
- `clear clipboard`

Calculator and converter:
- `calculate 25 plus 40`
- `calculate 12 times 8`
- `what is 100 divided by 4`
- `convert 10 dollars to taka`
- `convert 500 taka to dollars`

Apps:
- `open calculator`
- `open notepad`
- `open chrome`
- `open vs code`

Other:
- `time`
- `date`
- `news`
- ask any general question for the AI fallback

Daily briefing:
- `daily briefing`
- `morning briefing`
- `brief me`
- `start my day`

Custom routines:
- `create routine study mode: open vs code; play focus music; set timer for 25 minutes`
- `run routine study mode`
- `show routines`
- `delete routine study mode`

GUI:
- Run `python gui.py`
- Type commands, use the mic button, or use quick buttons for daily briefing, routines, and notes.

## Project Structure

- `main.py`: app loop and command router
- `gui.py`: desktop GUI for text and microphone commands
- `speech.py`: speech recognition and speaking
- `banglaCommands.py`: Bangla/Banglish command normalization
- `websites.py`: website shortcuts
- `search.py`: search engine commands
- `weather.py`: dynamic weather lookup
- `mediaLibrary.py`: media categories and YouTube search
- `reminders.py`: timer and reminder scheduler
- `briefing.py`: daily briefing with time, date, weather, and news
- `routines.py`: custom aliases and multi-command routines
- `memory.py`: persistent user memory
- `history.py`: local command history
- `system_control.py`: volume, mute, battery, screenshot, shutdown/restart confirmation
- `file_opener.py`: common folder opener
- `clipboard_helper.py`: clipboard read/copy/clear
- `calculator.py`: safe calculator and currency converter
- `notes.py`: local notes
- `apps.py`: local app launcher
- `news.py`: News API helper
- `ai_service.py`: OpenAI fallback
- `config.py`: environment-based settings
