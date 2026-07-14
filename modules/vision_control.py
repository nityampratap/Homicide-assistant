import pyautogui
import time
from PIL import ImageGrab

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

def capture_desktop_screen():
    """Captures the user's primary desktop screen and saves it temporarily."""
    print("[Vision Engine]: Taking screen snapshot...")
    screenshot = ImageGrab.grab()
    screenshot_path = "modules/temp_screen.png"
    screenshot.save(screenshot_path, "PNG")
    return screenshot_path

def fallback_os_app_launch(app_name):
    """Executes a native Windows UI hook to search and open an app if hidden from sight."""
    print(f"[OS System Search]: Querying Windows shell for -> {app_name}")
    
    pyautogui.press('win')
    time.sleep(0.6) # Let the start menu animation settle
    
    pyautogui.write(app_name.strip(), interval=0.03)
    time.sleep(0.5)
    pyautogui.press('enter')
    
    return f"Shortcut search executed for {app_name}."

def execute_screen_action(action_type, target_x, target_y, text_to_type=None):
    """Physically moves the mouse cursor to specific coordinates and handles clicks, double-clicks, and typing."""
    print(f"[OS Executing]: Action [{action_type}] at coordinate -> ({target_x}, {target_y})")
    
    x_coord = int(target_x)
    y_coord = int(target_y)
    
    # Smooth mouse move to targets
    pyautogui.moveTo(x_coord, y_coord, duration=0.4)
    time.sleep(0.1)
    
    if action_type.lower() == "double_click":
        pyautogui.doubleClick()
        return "Target double-clicked successfully."
        
    elif action_type.lower() == "click" or action_type.lower() == "type":
        pyautogui.click()
        time.sleep(0.2) # Give window focus time to catch up
        
        # If there is text attached to this visual action, type it and press Enter!
        if text_to_type:
            print(f"[OS Typing]: Writing text out -> {text_to_type}")
            pyautogui.write(text_to_type, interval=0.04)
            time.sleep(0.2)
            pyautogui.press('enter')
            return f"Clicked input area and searched for '{text_to_type}'."
            
        return "Target clicked successfully."
        
    return "Mouse position updated."