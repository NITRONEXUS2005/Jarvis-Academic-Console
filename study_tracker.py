import time
import json
import os
import ollama
import streamlit as st
from memory import get_subject_stats, add_study_session, load_memory
from exam_mode import launch_exam_mode
from voice import take_voice_command

MODEL = "llama3.2:1b"
FILE_NAME = "study_history.json"
TODO_FILE = "todo.json"

current_subject = None
current_topic = None
start_time = None

def append_to_ui(text):
    """Safely updates the live Streamlit UI console window log."""
    if "terminal_logs" in st.session_state:
        st.session_state.terminal_logs.append(text)

def safe_load():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def load_todo():
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_todo(data):
    with open(TODO_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_next_topic(subject):
    todos = load_todo()
    sub_clean = subject.lower().strip()
    if sub_clean in todos:
        for item in todos[sub_clean]:
            if not item["completed"]:
                return item["topic"]
    return "All listed core curriculum topics completed!"

def start_study(subject, actions=None):
    global current_subject, current_topic, start_time
    current_subject = subject.lower().strip()
    current_topic = get_next_topic(current_subject)
    start_time = time.time()

    msg = f"[System]: Active Subject: {current_subject.upper()} | Targeting Topic: {current_topic}"
    print(msg)
    append_to_ui(msg)
    
    try:
        import study_env
        study_env.enable_distraction_blocker()
    except ImportError:
        append_to_ui("[System Warning]: study_env.py not detected. Blocker bypassed.")
    
    if actions:
        actions.speak(f"Deep study mode initiated for {current_subject}. Today's target topic is: {current_topic}.")
        actions.play_music("stay with me:miki matsubara") 

def save_session(subject, duration):
    data = safe_load()
    session = {
        "subject": subject.lower().strip(),
        "duration_minutes": round(duration / 60, 2)
    }
    data.append(session)
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

def stop_study(actions=None):
    global current_subject, current_topic, start_time
    if start_time is None:
        append_to_ui("⚠️ System Alert: No active study session found to tear down.")
        return

    duration = time.time() - start_time
    duration_min = round(duration / 60, 2)

    msg = f"⏱️ Session Concluded. Studied {current_subject.upper()} for {duration_min:.2f} minutes."
    print(msg)
    append_to_ui(msg)

    try:
        import study_env
        study_env.disable_distraction_blocker()
    except ImportError:
        pass

    save_session(current_subject, duration)
    add_study_session(current_subject, duration_min)
    
    if actions and current_topic and "completed!" not in current_topic:
        actions.speak(f"Did you complete the topic: {current_topic}? Please say yes or no.")
        response = take_voice_command().lower().strip()
        
        # Fallback to simple text parsing if voice returns blank
        if not response and "cmd_input" in st.session_state:
            response = st.session_state.cmd_input.lower().strip()

        if "yes" in response or "yeah" in response:
            todos = load_todo()
            if current_subject in todos:
                for item in todos[current_subject]:
                    if item["topic"] == current_topic:
                        item["completed"] = True
                        actions.speak("Excellent. Marking this topic as completed.")
                        append_to_ui(f"✅ Topic Completed: {current_topic}")
                        save_todo(todos)
                        break
        else:
            actions.speak("Understood. Retaining topic position for your next tracking window.")

    current_subject = None
    current_topic = None
    start_time = None

def show_progress():
    data = safe_load()
    if not data:
        append_to_ui("📝 Progress Pipe: No historical study traces found.")
        return

    totals = {}
    for session in data:
        subject = session["subject"]
        duration = session["duration_minutes"]
        totals[subject] = totals.get(subject, 0) + duration

    out = "📊 **Current Study Progress Metrics:**\n"
    for subject, duration in totals.items():
        out += f"• {subject.upper()}: {duration:.2f} minutes\n"
    append_to_ui(out)

def show_subject_ranking():
    data = safe_load()
    if not data:
        append_to_ui("📝 Ranking Pipe: No historical stats compiled yet.")
        return

    totals = {}
    for session in data:
        subject = session["subject"]
        duration = session["duration_minutes"]
        totals[subject] = totals.get(subject, 0) + duration

    ranking = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    out = "🏆 **ECE Subject Attention Rankings:**\n"
    for i, (subject, duration) in enumerate(ranking, start=1):
        out += f"{i}. {subject.upper()} ({duration:.2f} total minutes)\n"
    append_to_ui(out)

def generate_suggestions():
    data = safe_load()
    if not data:
        append_to_ui("💡 System Suggestion: Add core syllabus files to begin optimization mapping.")
        return

    totals = {}
    for session in data:
        subject = session["subject"]
        duration = session["duration_minutes"]
        totals[subject] = totals.get(subject, 0) + duration

    weakest = min(totals, key=totals.get)
    out = f"💡 **Syllabus Optimization Strategy:**\nYour current bottleneck profile is **{weakest.upper()}**. We suggest launching exam prep modules for this domain next."
    append_to_ui(out)

def generate_ai_suggestions(speak=None):
    stats = get_subject_stats()
    if not stats:
        msg = "No study data available yet."
        append_to_ui(msg)
        if speak: speak(msg)
        return msg

    formatted = "\n".join([f"{s}: {t} min" for s, t in stats.items()])
    prompt = f"You are an AI study mentor for an ECE student.\n\nStudy history:\n{formatted}\n\nGive:\n- Weak subject analysis\n- What to study next\n- 1 motivation line\n\nKeep it short (max 10 lines)."

    try:
        response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
        result = response["message"]["content"].strip()
        append_to_ui(f"🤖 **Jarvis Mentor Recommendation:**\n{result}")
        if speak: speak(result)
        return result
    except Exception as e:
        append_to_ui(f"⚠️ AI Core error mapping trends: {e}")
        return ""

def resume_last_session(actions):
    memory_data = load_memory()
    last_subject = memory_data.get("last_subject")

    if not last_subject:
        actions.speak("I could not find any recent study session in my memory banks.")
        append_to_ui("⚠️ Resume State Failure: last_subject execution token is missing.")
        return 
    
    next_up = get_next_topic(last_subject)
    actions.speak(f"Tracking your history. You were last studying {last_subject}. Next target is {next_up}. Launching workspace.")
    append_to_ui(f"🔄 **Resuming Last Workspace State:** {last_subject.upper()}")
    
    start_study(last_subject, actions=actions)
    actions.init_driver()
    launch_exam_mode(last_subject, take_voice_command, actions.speak, actions.driver)