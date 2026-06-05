from exam_resources import exam_resources
import os

def launch_exam_mode(subject, take_voice_command, speak, driver):
    subject = subject.lower().strip()

    if subject not in exam_resources:
        speak("Subject not found in exam resources")
        print("Subject not found in exam resources")
        return

    resources = exam_resources[subject]
    speak(f"Exam mode activated for {subject}")

    print("\nWhat do you want to open?")
    print("Say: pdf, youtube, website, or all")
    speak("Say pdf, youtube, website, or all")

    choice = take_voice_command()
    choice = choice.lower().strip()

    # 1. Open PDF Locally
    if "pdf" in choice:
        if resources.get("pdf"):
            os.startfile(resources["pdf"])
            speak("Opening PDF notes")
        else:
            speak("No PDF available")

    # 2. Open YouTube Playlist
    elif "youtube" in choice:
        if resources.get("youtube") and driver:
            speak("Opening YouTube playlist")
            driver.get(resources["youtube"])
        else:
            speak("No YouTube link or browser available")

    # 3. Open ECE Website
    elif "website" in choice:
        if resources.get("website") and driver:
            speak("Opening website")
            driver.get(resources["website"])
        else:
            speak("No website available")

    # 4. Open All cleanly across separate Browser Tabs!
    elif "all" in choice:
        opened = False

        if resources.get("pdf"):
            os.startfile(resources["pdf"])
            opened = True

        if resources.get("youtube") and driver:
            driver.get(resources["youtube"]) # First link opens in Tab 1
            opened = True

        if resources.get("website") and driver:
            # Execute Javascript to cleanly open a completely new browser tab
            driver.execute_script(f"window.open('{resources['website']}', '_blank');")
            opened = True

        if opened:
            speak("Opening all available syllabus resources")
        else:
            speak("No resources available")

    else:
        speak("Command not recognized in exam mode")