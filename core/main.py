import os
import sys
import time
import re
from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(ROOT_DIR)

from modules.voice_output import speak
from modules.voice_input import wait_for_wake_word, listen_to_user
from modules.ai_brain import generate_vision_response
from modules.vision_control import capture_desktop_screen, execute_screen_action, fallback_os_app_launch

load_dotenv()

def main():
    print("🛡️ Security Verification: Continuous session matrix initialized.")
    speak("Homicide smart automation active.")
    
    while True:
        if wait_for_wake_word():
            speak("Homicide activated. Listening for continuous commands.")
            
            while True:
                screen_file = capture_desktop_screen()
                command = listen_to_user()
                
                if command:
                    print(f"\n🎙️ [Active Directive]: '{command}'")
                    cmd_lower = command.lower().strip()
                    
                    if any(phrase in cmd_lower for phrase in ["deactivate homicide", "deactivate", "shutdown", "stop listening", "go to sleep"]):
                        speak("Deactivating Homicide. Returning to standby mode.")
                        if os.path.exists(screen_file):
                            os.remove(screen_file)
                        break

                    print("[Analyzing screen perspective...]")
                    ai_reply = generate_vision_response(command, screen_file)
                    print(f"[Brain Cleaned Output]: {ai_reply}")

                    # --- COMMAND ROUTING LAYER ---
                    if ai_reply.startswith("JSON_YOUTUBE_SEARCH:"):
                        query = ai_reply.replace("JSON_YOUTUBE_SEARCH:", "").strip()
                        execution_msg = execute_screen_action("youtube_search", 0, 0, text_to_type=query)
                        speak(execution_msg)

                    elif ai_reply.startswith("JSON_FALLBACK_LAUNCH:"):
                        target_app = ai_reply.replace("JSON_FALLBACK_LAUNCH:", "").strip()
                        execution_msg = fallback_os_app_launch(target_app)
                        speak(execution_msg)
                        time.sleep(1.5)
                    
                    elif ai_reply.startswith("JSON_TYPE:"):
                        payload = ai_reply.replace("JSON_TYPE:", "").strip()
                        if "|" in payload:
                            parts = payload.split("|", 2)
                            if len(parts) == 3:
                                x, y, text_string = parts
                                execution_msg = execute_screen_action("type", x, y, text_to_type=text_string)
                                speak(execution_msg)
                    
                    elif ai_reply.startswith("JSON_DOUBLE_CLICK:"):
                        payload = ai_reply.replace("JSON_DOUBLE_CLICK:", "").strip()
                        if "|" in payload:
                            x, y = payload.split("|", 1)
                            execution_msg = execute_screen_action("double_click", x, y)
                            speak(execution_msg)
                    
                    elif ai_reply.startswith("JSON_CLICK:"):
                        payload = ai_reply.replace("JSON_CLICK:", "").strip()
                        if "|" in payload:
                            x, y = payload.split("|", 1)
                            execution_msg = execute_screen_action("click", x, y)
                            speak(execution_msg)
                    else:
                        print(f"[Homicide AI]: {ai_reply}")
                        speak(ai_reply)

                    if os.path.exists(screen_file):
                        os.remove(screen_file)

                else:
                    print("[Session Active]: Standing by for your next directive...")
                    if os.path.exists(screen_file):
                        os.remove(screen_file)

if __name__ == "__main__":
    main()