from seleniumbase import Driver
from music_library import music
import voice  # Import your voice file directly

driver = None
# Set your thread-safe speaker function as the structural default fallback
speak = voice.speak  

def set_voice(speak_func):
    global speak
    speak = speak_func

def init_driver():
    global driver
    try:
        if driver is None:
            driver = Driver(uc=False)
        else:
            # Touch the current URL to verify if the window is still open
            driver.current_url
    except Exception:
        driver = Driver(uc=False)            

def open_google():
    init_driver()
    speak("Opening Google")
    driver.get("https://www.google.com")

def open_youtube():
    init_driver()
    speak("Opening YouTube")
    driver.get("https://www.youtube.com")

def play_music(song_name):
    init_driver()
    song_name = song_name.strip().lower()

    if song_name in music:
        speak(f"Playing {song_name}")
        driver.get(music[song_name])
    else:
        speak("Song is not found in the library")
        search_url = "https://www.youtube.com/results?search_query=" + song_name.replace(" ", "+")
        driver.get(search_url) 

def show_help():
    commands = """
Available Commands:
Open Google
Open YouTube
Play <song name>
Start Study <subject>
Stop Study
Show Progress
Subject Ranking
Study Suggestion
Exam Mode <subject>
Explain <topic>
Summarize <topic>
Generate Questions <topic>
"""        
    print(commands)
    if speak:
        speak("I can open websites, play music, track study sessions, launch exam mode, and assist with academic preparation.")