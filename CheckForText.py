import keyboard
import pyautogui
import pyperclip
import time

def copy_input_text():
    if keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt') or keyboard.is_pressed('shift'):
        return

    pyautogui.hotkey('ctrl', 'a', interval=0.001)
    pyautogui.hotkey('ctrl', 'c', interval=0.001)

    copied_text = pyperclip.paste()
    print(copied_text)

    # Click at the current mouse location to deselect
    pyautogui.click()

keyboard.add_hotkey('F12', copy_input_text)
keyboard.wait('esc')
