import speech_recognition as sr

def wait_for_wake_word():
    """
    Listens continuously in a localized background loop for your 
    specific secure activation phrase to wake up the assistant.
    """
    r = sr.Recognizer()
    
    # Access the primary system microphone safely
    with sr.Microphone() as source:
        # Dynamically adjust to ambient room noise so it doesn't misfire
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("\n[System Online - Streaming mic smoothly for 'Activate Homicide'...]")
        
        try:
            # Listen to the audio stream without a timeout to keep it running forever
            audio = r.listen(source, timeout=None, phrase_time_limit=3)
            
            # Process voice locally/cloud via standard en-IN matching for English/Hindi accents
            text = r.recognize_google(audio, language="en-IN").lower().strip()
            
            # Check if the user spoke the strict wake word blueprint
            if "activate homicide" in text:
                return True
        except Exception:
            # Fail silently to keep the background loop streaming without crashing
            pass
            
    return False

def listen_to_user():
    """
    Accesses the microphone to record your primary automation command 
    once the master activation sequence clears.
    """
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("[Homicide is listening for your directive...]")
        
        try:
            # Capture speech with a strict limit to ensure fast execution response times
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            print("[Processing speech via cloud matrix...]")
            
            # Transcribe the command using the free multilingual translation schema
            command = r.recognize_google(audio, language="en-IN")
            return command
            
        except sr.UnknownValueError:
            # Triggers if the microphone hears static or muffled background sounds
            return None
        except Exception as e:
            print(f"❌ Audio Stream Error: {e}")
            return None