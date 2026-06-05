import ollama
import re
import streamlit as st

MODEL = "llama3.2:1b"

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