
import time
import pyautogui
'''
print(pyautogui.position())
pyautogui.moveTo(100, 100, duration=1)
pyautogui.click(100, 100)
pyautogui.rightClick(100, 100)
pyautogui.scroll(-500)
time.sleep(2)

#keyboard
pyautogui.write('Hello world!', interval=0.1)
pyautogui.press('enter')
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
pyautogui.hotkey('ctrl', 'v')
pyautogui.press('enter')
time.sleep(2)
'''
#Keyboard

# pyautogui.click(638, 294)

# time.sleep(2)
# pyautogui.hotkey('ctrl', 'a')
# pyautogui.hotkey('ctrl', 'c')
# pyautogui.press('enter')
# pyautogui.hotkey('ctrl', 'v')
# pyautogui.hotkey('ctrl', 's')
# pyautogui.press('enter')
# time.sleep(2)

#image recognition

# location = pyautogui.locateOnScreen('ads.png', confidence=0.8)
# print(location)
# pyautogui.click(pyautogui.center(location))
windows = pyautogui.size()
print(windows)
