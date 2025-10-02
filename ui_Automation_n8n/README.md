# Notepad Automation

This small script uses PyAutoGUI to open Notepad, append user-provided text to a file named `localeagel.txt`, save, and close Notepad.

Requirements
- Python 3.8+
- Windows (script uses Win+R to open Run dialog)

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Usage:

Command-line usage (legacy):

```powershell
python .\notepad_automation.py "your text here"
```

Flask API usage (new):

Start the server:

```powershell
python .\notepad_automation.py
```

POST JSON to append text and open Notepad (default):

```powershell
curl -X POST http://127.0.0.1:5000/write -H "Content-Type: application/json" -d '{"text":"hello from api"}'
```

To append without opening Notepad:

```powershell
curl -X POST http://127.0.0.1:5000/write -H "Content-Type: application/json" -d '{"text":"no ui", "open": false}'
```

Notes:
- The script prefers `pyperclip` for reliable clipboard pastes. If `pyperclip` is not installed it will type the text which may be slower and less reliable for special characters.
- The script uses simple sleeps and key sequences; ensure your machine is not performing other interactive tasks while it runs.
