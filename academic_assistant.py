import ollama
import re
import streamlit as st

MODEL = "llama3.2:1b"


import streamlit as st
import numpy as np
import plotly.graph_objects as go

def render_ece_simulation(topic):
    topic = topic.lower().strip()
    
    if "ohms law" in topic:
        st.markdown("### 📈 Subsystem Matrix: Ohm's Law Verification")
        st.latex(r"I = \frac{V}{R} \quad \text{or} \quad V = I \cdot R")
        
        # Interactive Simulation Plotly Logic
        resistance = st.slider("Adjust Circuit Resistance (Ohms)", min_value=1, max_value=100, value=10)
        voltage = np.linspace(0, 12, 100)
        current = voltage / resistance
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name=f'R = {resistance} Ω', line=dict(color='#00FFCC')))
        fig.update_layout(title="Linear I-V Characteristic Curve", xaxis_title="Voltage (V)", yaxis_title="Current (A)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif "semiconductor" in topic or "diode" in topic:
        st.markdown("### 🧬 Subsystem Matrix: Diode Shockley Equation")
        st.latex(r"I = I_S \left( e^{\frac{qV}{nkT}} - 1 \right)")
        
        # Simulate non-linear diode curve
        v_diode = np.linspace(-1.0, 0.8, 200)
        Is = 1e-12  # Saturation current
        Vt = 0.026  # Thermal voltage at room temp
        i_diode = Is * (np.exp(v_diode / (1 * Vt)) - 1)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=v_diode, y=i_diode, mode='lines', name='Diode Conduction State', line=dict(color='#FF3366')))
        fig.update_layout(title="Non-Linear Diode I-V Curve", xaxis_title="Diode Voltage (V)", yaxis_title="Current (A)", yaxis=dict(range=[-1e-9, 0.01]), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

def append_to_ui(text):
    """Safely updates the live Streamlit UI log monitor."""
    if "terminal_logs" in st.session_state:
        st.session_state.terminal_logs.append(text)

def speak_in_chunks(text, speak):
    if not speak:
        return

    # FIXED REGEX: Removed the illegal '**' multiplier
    chunks = re.split(r'(?<=[.!?])\s+', text)

    for chunk in chunks:
        chunk = chunk.strip()
        if chunk:
            speak(chunk)

def explain_topic(topic, speak):
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"Explain {topic} in a simple and exam-friendly way for an ECE student in short points suitable for speaking."
            }]
        )
        result = response["message"]["content"].strip()
        
        # Log to UI immediately before trying to speak
        append_to_ui(f"🤖 **Jarvis (Explanation):**\n{result}")
        speak_in_chunks(result, speak)
        return result
        
    except Exception as e:
        # This will now catch actual failures instead of your regex syntax crash
        print("AI Error:", e)
        append_to_ui(f"⚠️ AI Core Processing Error: {e}")
        speak("Sorry, I couldn't process that request.")
        return ""

def summarize_topic(topic, speak):
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"Give a short bullet point summary of {topic} suitable for voice reading."
            }]
        )
        result = response["message"]["content"].strip()
        
        append_to_ui(f"🤖 **Jarvis (Summary):**\n{result}")
        speak_in_chunks(result, speak)
        return result
    except Exception as e:
        print("AI Error:", e)
        append_to_ui(f"⚠️ AI Summary Error: {e}")
        speak("Sorry, I couldn't generate summary.")
        return ""

def generate_questions(topic, speak):
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{
                "role": "user",
                "content": f"Generate important exam questions and answers for {topic} (ECE level) in short readable format."
            }]
        )
        result = response["message"]["content"].strip()
        
        append_to_ui(f"🤖 **Jarvis (Revision Questions):**\n{result}")
        speak_in_chunks(result, speak)
        return result
    except Exception as e:
        print("AI Error:", e)
        append_to_ui(f"⚠️ AI Question Generator Error: {e}")
        speak("Sorry, I couldn't generate questions.")
        return ""