import pyautogui
import time
import webbrowser

# Enable PyAutoGUI failsafe (move mouse to top-left to stop the script)
pyautogui.FAILSAFE = True

# Step 1: Open Chrome (or default browser)
webbrowser.open("https://www.google.com")
time.sleep(5)  # wait for the browser to open fully

# Step 2: Type search text
pyautogui.typewrite("social eagle", interval=0.1)
pyautogui.press("enter")
time.sleep(5)  # wait for results to load

# Step 3: Move to first result and click
# (This part may depend on your screen size)
# Usually, the first result appears around the top of the screen
pyautogui.moveTo(351, 522, duration=1)  # adjust X, Y coordinates if needed
pyautogui.click()
