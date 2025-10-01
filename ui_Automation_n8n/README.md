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

```powershell
python .\notepad_automation.py "your text here"
```

Notes:
- The script prefers `pyperclip` for reliable clipboard pastes. If `pyperclip` is not installed it will type the text which may be slower and less reliable for special characters.
- The script uses simple sleeps and key sequences; ensure your machine is not performing other interactive tasks while it runs.
