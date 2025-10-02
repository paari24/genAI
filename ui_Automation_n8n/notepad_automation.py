from flask import Flask, request, jsonify
import pyautogui
import time
import os
from typing import Optional

app = Flask(__name__)

# Small defaults to make key sequences less brittle
pyautogui.PAUSE = 0.12
pyautogui.FAILSAFE = True

FILE_NAME = "localeagel.txt"


def append_text_to_file(text: str) -> Optional[str]:
    """Append text to FILE_NAME, flush and fsync, then return the last line read back.
    Returns the last line (without newline) or None on error.
    """
    file_path = os.path.abspath(FILE_NAME)
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(text + "\n")
            f.flush()
            try:
                os.fsync(f.fileno())
            except Exception:
                pass
    except Exception as e:
        app.logger.exception("Error writing to file")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_line = lines[-1].rstrip('\n') if lines else ''
            return last_line
    except Exception:
        app.logger.exception("Error reading file back")
        return None


def open_and_close_notepad(file_path: str):
    """Open Notepad with the file path and close it. Non-blocking UI actions with small waits."""
    run_cmd = f'notepad "{file_path}"'
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)
    pyautogui.write(run_cmd)
    pyautogui.press('enter')
    time.sleep(1.2)
    try:
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.2)
        pyautogui.press('enter')
    except Exception:
        app.logger.exception('Failed to close Notepad via pyautogui')


@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "ok", "file": FILE_NAME})


@app.route('/write', methods=['POST'])
def write_endpoint():
    """POST JSON {"text": "...", "open": true/false}

    - text: required string to append
    - open: optional boolean (default true) whether to open Notepad after writing
    """
    data = request.get_json(silent=True) or request.form
    text = data.get('text') if isinstance(data, dict) else None
    if not text:
        return jsonify({"error": "'text' is required in JSON body or form data"}), 400

    last_line = append_text_to_file(text)
    if last_line is None:
        return jsonify({"error": "failed to write to file"}), 500

    open_flag = True
    if isinstance(data, dict):
        open_flag = bool(data.get('open', True))
    else:
        open_flag = data.get('open', 'true').lower() in ('1', 'true', 'yes') if data.get('open') is not None else True

    file_path = os.path.abspath(FILE_NAME)
    if open_flag:
        # open and close Notepad to satisfy the UI requirement
        open_and_close_notepad(file_path)

    response = {
        'status': 'ok',
        'file': file_path,
        'last_line': last_line,
    }
    return jsonify(response)


if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='127.0.0.1', port=5000)