import pyautogui
import time
import sys
import os

# Small defaults to make key sequences less brittle
pyautogui.PAUSE = 0.12
pyautogui.FAILSAFE = True


def write_to_notepad(user_input: str):
    """Append the user input to `localeagel.txt` (guaranteed file write),
    then open Notepad to display the file and close it.

    Rationale: GUI typing/paste can be flaky. Writing directly to the file ensures
    the content is saved. Opening Notepad afterward satisfies the requirement to
    open the file in Notepad and then close it.
    """
    file_name = "localeagel.txt"
    file_path = os.path.abspath(file_name)

    # Append to the file (guaranteed save)
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(user_input + "\n")
            f.flush()
            # ensure data is written to disk
            try:
                os.fsync(f.fileno())
            except Exception:
                # fsync may not be available on all platforms but on Windows it's fine
                pass
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        raise

    # Verify the last line was written correctly
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_line = lines[-1].rstrip('\n') if lines else ''
    except Exception as e:
        print(f"Error reading back {file_path}: {e}")
        last_line = None

    if last_line == user_input:
        print(f"Successfully wrote to {file_path}: '{last_line}'")
    else:
        print(f"Warning: last line in {file_path!r} does not match input. last_line={last_line!r}")

    # Open Notepad with the full path so the saved content is visible
    # Use quotes around the path to handle spaces
    run_cmd = f'notepad "{file_path}"'
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)
    pyautogui.write(run_cmd)
    pyautogui.press('enter')
    # give Notepad time to open and render the file
    time.sleep(1.2)

    # Close Notepad cleanly
    try:
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.2)
        # In case a prompt appears (shouldn't, since file is already saved), confirm
        pyautogui.press('enter')
    except Exception as e:
        print(f"Error while trying to close Notepad: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python notepad_automation.py \"your text here\"")
        sys.exit(1)

    # Join all args so multi-word inputs work as expected
    user_input = " ".join(sys.argv[1:])
    write_to_notepad(user_input)