import streamlit as st
import time
from brain import process_command
import actions

st.set_page_config(page_title="Jarvis Academic Assistant", layout="wide", page_icon="🤖")

if "terminal_logs" not in st.session_state:
    st.session_state.terminal_logs = []

st.title("🤖 Jarvis: ECE Academic Workspace Matrix")
st.markdown("---")

# --- NEW SIDEBAR FEATURE: FORMULA CHEAT SHEET HUDBoard ---
with st.sidebar:
    st.header("🗂️ Rapid Formula Reference Matrix")
    st.markdown("Click components below for structural math syntax profiles:")
    
    with st.expander("⚡ Network Theory & AC Circuits"):
        st.markdown("**Impedance Vector:**")
        st.latex(r"Z = R + jX_L - jX_C")
        st.markdown("**Resonant Frequency:**")
        st.latex(r"f_0 = \frac{1}{2\pi\sqrt{LC}}")
        
    with st.expander("📡 Signal Processing & Communications"):
        st.markdown("**Shannon Channel Capacity:**")
        st.latex(r"C = B \log_2\left(1 + \frac{S}{N}\right)")
        st.markdown("**Fourier Transform Pair:**")
        st.latex(r"X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi ft} dt")

    with st.expander("🧬 Semiconductor Microelectronics"):
        st.markdown("**Intrinsic Carrier Concentration:**")
        st.latex(r"n_i^2 = N_C N_V e^{-\frac{E_g}{kT}}")

# Main Split Workspace Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("⚙️ System Command Terminal Interface")
    st.markdown("*Try running commands like `explain rc circuit`, `explain ohms law`, or `explain diode` to boot dynamic visual test-benches.*")
    text_command = st.text_input("Enter strategic matrix command or prompt:", placeholder="e.g., explain rc circuit")
    
    if st.button("Execute Core Command", use_container_width=True):
        if text_command.strip():
            st.session_state.terminal_logs.append(f"👤 **User:** {text_command}")
            with st.spinner("Processing framework logic..."):
                process_command(text_command.lower().strip(), actions)
            st.rerun()

with col2:
    st.subheader("📟 Live Subsystem Log Monitor")
    if st.button("Clear Console History", use_container_width=True):
        st.session_state.terminal_logs = []
        st.rerun()
        
    st.markdown("---")
    for log in reversed(st.session_state.terminal_logs):
        st.markdown(log)