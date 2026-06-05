import json
import os 
from datetime import datetime

FILE_NAME = "memory.json"

def load_memory():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except:
            pass
            
    return {
        "study_history": [],
        "last_subject": "None Logged"
    }  

def save_memory(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

def add_study_session(subject, duration_minutes):
    data = load_memory()
    session = {
        "subject": subject.lower().strip(),
        "duration": duration_minutes,
        "time": str(datetime.now())
    }    
    data["study_history"].append(session)
    data["last_subject"] = subject.lower().strip()
    save_memory(data)

def get_summary():
    return load_memory()

def get_subject_stats():
    data = load_memory()
    stats = {}
    for session in data.get("study_history", []):
        subject = session["subject"]
        duration = session["duration"]
        stats[subject] = stats.get(subject, 0) + duration
    return stats