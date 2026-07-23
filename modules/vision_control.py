import pyautogui
import time
import re
from PIL import ImageGrab

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

def capture_desktop_screen():
    """Captures the primary desktop screen and saves it temporarily."""
    print("[Vision Engine]: Taking screen snapshot...")
    screenshot = ImageGrab.grab()
    screenshot_path = "modules/temp_screen.png"
    screenshot.save(screenshot_path, "PNG")
    return screenshot_path

def fallback_os_app_launch(app_name):
    """Executes a native Windows UI hook to search and open an app reliably."""
    print(f"[OS System Search]: Querying Windows shell for -> {app_name}")
    
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write(app_name.strip(), interval=0.03)
    time.sleep(0.4)
    pyautogui.press('enter')
    
    return f"Opening {app_name} via system search."

def execute_screen_action(action_type, target_x, target_y, text_to_type=None):
    """Executes mouse clicks or typing at specific coordinates with sanitization."""
    
    clean_x = re.sub(r'[^\d]', '', str(target_x))
    clean_y = re.sub(r'[^\d]', '', str(target_y))
    
    x_coord = int(clean_x) if clean_x else 500
    y_coord = int(clean_y) if clean_y else 500
    
    if action_type.lower() == "youtube_search" and text_to_type:
        print(f"[YouTube Shortcut]: Pressing '/' to focus YouTube search bar...")
        pyautogui.press('/')
        time.sleep(0.3)
        # Select all and delete any pre-existing query text
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        time.sleep(0.1)
        pyautogui.write(text_to_type, interval=0.04)
        time.sleep(0.2)
        pyautogui.press('enter')
        return f"Searched YouTube for '{text_to_type}' using native shortcuts."

    print(f"[OS Executing]: Moving mouse to ({x_coord}, {y_coord}) for action: {action_type}")
    pyautogui.moveTo(x_coord, y_coord, duration=0.4)
    time.sleep(0.1)
    
    if action_type.lower() == "click":
        pyautogui.click()
        return "Target clicked successfully."
    elif action_type.lower() == "double_click":
        pyautogui.doubleClick()
        return "Target double-clicked successfully."
    elif action_type.lower() == "type" and text_to_type:
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.write(text_to_type, interval=0.04)
        pyautogui.press('enter')
        return f"Typed '{text_to_type}' and submitted."
        
    return "Action executed."