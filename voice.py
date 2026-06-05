import pyttsx3
import threading
import speech_recognition as sr

# Global lock to prevent overlapping audio thread crashes
_engine_lock = threading.Lock()

def speak(text):
    print(f"Jarvis: {text}")
    
    def target():
        with _engine_lock:
            try:
                # Initialize engine inside the background worker thread
                engine = pyttsx3.init()
                engine.setProperty('rate', 175)  # Natural speaking rate
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"[TTS Thread Warning]: {e}")

    # Fire and forget the speaker on a separate thread
    threading.Thread(target=target, daemon=True).start()

def take_voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[System Listening...]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Added a tight timeout so your web panel never freezes indefinitely
            audio = r.listen(source, timeout=4, phrase_time_limit=4)
            print("[System Recognizing...]")
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except Exception:
            return ""