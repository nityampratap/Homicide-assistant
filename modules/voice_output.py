import pyttsx3

def speak(text):
    """Gives Homicide a voice response using local TTS."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Index 0 is usually a crisp male/system voice. 
        # Change to voices[1].id if you prefer a different default system voice.
        engine.setProperty('voice', voices[0].id) 
        engine.setProperty('rate', 175)  # Speeds up speech slightly for a sharper tone
        
        print(f"[Homicide]: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in Text-to-Speech: {e}")