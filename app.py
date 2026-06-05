import streamlit as st
import os
import json
import subprocess
import actions  # Import your actions file directly as a module
from brain import process_command
from study_tracker import load_todo, get_next_topic

# --- CONFIGURATION & CYBERPUNK DARK THEME ---
st.set_page_config(page_title="Jarvis OS Console", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { 
        background-color: #21262d; 
        color: #58a6ff; 
        border: 1px solid #30363d; 
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #30363d; border-color: #8b949e; color: #58a6ff; }
    h1, h2, h3, h4 { color: #58a6ff !important; font-family: 'Courier New', Courier, monospace; }
    .status-box { 
        border: 1px solid #30363d; 
        padding: 20px; 
        border-radius: 8px; 
        background-color: #161b22;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


if "jarvis_actions" not in st.session_state:
    # 1. Import your voice engine speaking function
    try:
        from voice import speak as voice_speak
        actions.set_voice(voice_speak) # Link it to your actions framework
    except ImportError:
        pass
    
    st.session_state.jarvis_actions = actions
if "terminal_logs" not in st.session_state:
    st.session_state.terminal_logs = ["[System Initialization]: Jarvis Control Panel Online."]

actions_mod = st.session_state.jarvis_actions
# --- MAIN HEADER ---
st.title("⚡ Jarvis Academic Control Center")
st.caption("Integrated Local AI Console & ECE syllabus Optimization Engine")
st.markdown("---")

# --- UI SPLIT LAYOUT ---
col1, col2 = st.columns([5, 3])

# --- COLUMN 1: INTERACTIVE COMMAND CONSOLE ---
with col1:
    st.subheader("⌨️ System Input Interface")
    
    # 1. Silent Keyboard Mode
    text_command = st.text_input("Type a direct command here (e.g., 'explain diode' or 'start study oop'):", key = "cmd input")
    
    if st.button("Execute Command") and text_command:
        st.session_state.terminal_logs.append(f"👤 User (Text): {text_command}")
        with st.spinner("Processing intent pipeline..."):
            process_command(text_command, actions_mod)  # Pass the module reference
        st.rerun()

    st.markdown("### 🎙️ Hardware Macro Controls")
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        # 2. Hands-Free Mic Bypass Button
        if st.button("🎤 Trigger Microphone (Skip Wake Word)", use_container_width=True):
            st.session_state.terminal_logs.append("🔊 System Mic Activated... Listening...")
            from voice import take_voice_command
            cmd = take_voice_command()
            if cmd:
                st.session_state.terminal_logs.append(f"👤 User (Voice): {cmd}")
                with st.spinner("Executing verbal pipeline..."):
                  process_command(cmd,actions_mod)
            else:
                st.session_state.terminal_logs.append("⚠️ System Warning: Silence detected or audio unparseable.")
            st.rerun()
                
    with v_col2:
        # 3. One-Click Quick Resume Macro
        if st.button("🔄 Fast Progress Trackback (Resume Last)", use_container_width=True):
            st.session_state.terminal_logs.append("👤 Macro Triggered: Resume Last Session State")
            with st.spinner("Accessing database state locks..."):
                process_command("resume study", actions_mod)
            st.rerun()

    # 4. Interactive Terminal Output Box
    st.markdown("### 📜 Live Console Feed Log")
    log_content = "\n".join(st.session_state.terminal_logs[-8:])  # Limit window view to last 8 logs
    st.text_area("System Log Pipe", value=log_content, height=220, disabled=True)


# --- COLUMN 2: REAL-TIME SYSTEM DIAGNOSTIC MONITOR ---
with col2:
    st.subheader("📊 Dynamic Engine Diagnostics")
    
    # Read backend JSON database parameters live on page refresh
    if os.path.exists("memory.json"):
        try:
            with open("memory.json", "r") as f:
                mem_data = json.load(f)
        except:
            mem_data = {}
    else:
        mem_data ={}
        
    last_sub = mem_data.get("last_subject", "None Logged")
    next_topic_up = get_next_topic(last_sub) if last_sub != "None Logged" else "N/A"

    # Display Engine Status Card
    st.markdown(f"""
    <div class="status-box">
        <h4 style='margin-top:0;'>💡 Local AI Status Block</h4>
        <p><b>Cognitive LLM Engine:</b> <span style='color:#7ee787;'>llama3.2:1b (Ollama)</span></p>
        <p><b>Automation Controller:</b> <span style='color:#7ee787;'>SeleniumBase WebDriver</span></p>
        <hr style='border-color:#30363d;'>
        <h4>🧠 Last Known State Bookmarks</h4>
        <p><b>Subject Parameter:</b> <span style='color:#58a6ff;'>{last_sub.upper()}</span></p>
        <p style='margin-bottom:0;'><b>Next Look-Ahead Target:</b> <span style='color:#db6d28;'>{next_topic_up}</span></p>
    </div>
    """, unsafe_allow_html = True)
    
    # 5. Live Syllabus Progress Bars
    st.markdown("### 📈 Roadmao completion percentages")
    todos = load_todo()
    if todos:
        for subj, items in todos.items():
            if items:
                completed_count = sum(1 for i in items if i["completed"])
                total_count = len(items)
                pct = completed_count / total_count
                st.progress(pct, text=f"**{subj.upper()}** ({completed_count}/{total_count} Topics)")
    else:
        st.info("Drop topics into todo.json to track syllabus progress curves.")

    st.markdown("### 🛠️ Subsystem Hub")
    if st.button("📊 Launch Graphical Analysis Dashboard", use_container_width=True):
        st.success("Spawning visualization server charts in background tab...")
        subprocess.Popen(["streamlit", "run", "dashboard.py", "--server.port", "8502"])