import os
import sys
import time
from dotenv import load_dotenv

# Ensure system path resolution for internal modules
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
        # STEP 1: Wait silently in standby mode for the wake word
        if wait_for_wake_word():
            speak("Homicide activated. Listening for continuous commands.")
            
            # STEP 2: Continuous Active Mode Loop (Stays open until deactivated!)
            while True:
                # Take a fresh screenshot for every continuous command
                screen_file = capture_desktop_screen()
                command = listen_to_user()
                
                if command:
                    print(f"\n🎙️ [Active Directive]: '{command}'")
                    cmd_lower = command.lower().strip()
                    
                    # CHECK FOR DEACTIVATION COMMAND
                    if any(phrase in cmd_lower for phrase in ["deactivate homicide", "deactivate", "shutdown", "stop listening", "go to sleep"]):
                        speak("Deactivating Homicide. Returning to standby mode.")
                        if os.path.exists(screen_file):
                            os.remove(screen_file)
                        break  # Exits the active session loop, back to standby!

                    print("[Analyzing screen perspective...]")
                    ai_reply = generate_vision_response(command, screen_file)
                    print(f"[Brain Raw Output]: {ai_reply}")

                    # --- COMMAND ROUTING LAYER ---
                    
                    # 1. Native App Opener
                    if ai_reply.startswith("JSON_FALLBACK_LAUNCH:"):
                        target_app = ai_reply.replace("JSON_FALLBACK_LAUNCH:", "").strip()
                        execution_msg = fallback_os_app_launch(target_app)
                        speak(execution_msg)
                        time.sleep(1.5)  # Window focus stabilization delay
                    
                    # 2. Typing / Search Box Input
                    elif ai_reply.startswith("JSON_TYPE:"):
                        payload = ai_reply.replace("JSON_TYPE:", "").strip()
                        if "|" in payload:
                            parts = payload.split("|", 2)
                            if len(parts) == 3:
                                x, y, text_string = parts
                                execution_msg = execute_screen_action("type", x, y, text_to_type=text_string)
                                speak(execution_msg)
                    
                    # 3. Double Click
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
                    
                    # 5. General Speech / Analysis Response
                    else:
                        print(f"[Homicide AI]: {ai_reply}")
                        speak(ai_reply)

                    # Clean up temporary screenshot
                    if os.path.exists(screen_file):
                        os.remove(screen_file)

                else:
                    # If silence or unparseable speech occurs, stay in the active session
                    print("[Session Active]: Standing by for your next directive...")
                    if os.path.exists(screen_file):
                        os.remove(screen_file)

if __name__ == "__main__":
    main()