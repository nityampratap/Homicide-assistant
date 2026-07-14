import os
import sys
import time
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
    print("🛡️ Security Verification: Vision fallback system tracking matrix linked.")
    speak("Homicide smart automation active.")
    
    while True:
        if wait_for_wake_word():
            screen_file = capture_desktop_screen()
            speak("Online.")
            command = listen_to_user()
            
            if command:
                print(f"[User Voice Input]: {command}")
                cmd_lower = command.lower()
                
                if "shutdown" in cmd_lower:
                    speak("Homicide offline.")
                    if os.path.exists(screen_file):
                        os.remove(screen_file)
                    break
                
                print("[Analyzing screen perspective...]")
                ai_reply = generate_vision_response(command, screen_file)
                print(f"[Brain Raw Output]: {ai_reply}")
                
                # CRITICAL INTERCEPTION LAYER: Handle 429 Quota Blocks & 503 Spikes
                if "429" in ai_reply or "resource_exhausted" in ai_reply.lower():
                    print("⚠️ [Quota Block]: Hit Google API rate limits. Standing down brief moment.")
                    speak("Brain quota exhausted. Please wait a few seconds before reactivating.")
                    
                elif "503" in ai_reply or "brain error" in ai_reply.lower():
                    if "open" in cmd_lower or "launch" in cmd_lower:
                        target_app = cmd_lower.replace("open", "").replace("launch", "").replace("browser", "").strip()
                        execution_msg = fallback_os_app_launch(target_app)
                        speak(execution_msg)
                        time.sleep(1.5)
                    else:
                        speak("Cloud matrix busy. Please try your search request again.")
                
                # 1. Native App Opener
                elif ai_reply.startswith("JSON_FALLBACK_LAUNCH:"):
                    target_app = ai_reply.replace("JSON_FALLBACK_LAUNCH:", "").strip()
                    execution_msg = fallback_os_app_launch(target_app)
                    speak(execution_msg)
                    time.sleep(1.5)
                
                # 2. Text Search/Input Routine
                elif ai_reply.startswith("JSON_TYPE:"):
                    payload = ai_reply.replace("JSON_TYPE:", "").strip()
                    if "|" in payload:
                        parts = payload.split("|", 2)
                        if len(parts) == 3:
                            x, y, text_string = parts
                            execution_msg = execute_screen_action("type", x, y, text_to_type=text_string)
                            speak(execution_msg)
                
                # 3. Double Click Command
                elif ai_reply.startswith("JSON_DOUBLE_CLICK:"):
                    payload = ai_reply.replace("JSON_DOUBLE_CLICK:", "").strip()
                    if "|" in payload:
                        x, y = payload.split("|", 1)
                        execution_msg = execute_screen_action("double_click", x, y)
                        speak(execution_msg)
                
                # 4. Standard Single Click
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
                speak("Directive unclear.")

if __name__ == "__main__":
    main()