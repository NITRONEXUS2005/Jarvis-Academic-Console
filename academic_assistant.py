import streamlit as st
import numpy as np
import plotly.graph_objects as go

def explain_topic(topic, speak_fn=None):
    """Fallback text simulation engine for local academic context."""
    topic_clean = topic.lower().strip()
    st.markdown(f"### 🧠 Local Core Processing: Contextual Review for '{topic.upper()}'")
    
    if "ohms law" in topic_clean:
        res = "Ohm's Law establishes that the current passing through a conductor between two points is directly proportional to the voltage across the two points, governed by linear resistance."
    elif "filter" in topic_clean or "rc circuit" in topic_clean:
        res = "An RC Filter network selectively attenuates signal frequency components. Low-pass configurations let DC and low frequencies pass while blocking high-frequency noise profiles."
    elif "semiconductor" in topic_clean or "diode" in topic_clean:
        res = "Semiconductor diodes allow current to flow easily in one direction (forward bias) while blocking it in the reverse direction, governed exponentially by the Shockley diode equation."
    else:
        res = f"Localized systemic overview generated for {topic}. Ensure physical parameters match your modular ECE lab criteria."
        
    st.write(res)
    if speak_fn:
        try: 
            speak_fn(res[:60])  # Speak a short snippet safely
        except: 
            pass

def render_ece_simulation(topic):
    """Dynamically generates ECE interactive circuit simulation parameters and math matrices."""
    topic = topic.lower().strip()
    
    # --- FEATURE 1: OHM'S LAW VECTOR ENGINE ---
    if "ohms law" in topic:
        st.markdown("### 📈 Subsystem Matrix: Ohm's Law Verification")
        st.latex(r"I = \frac{V}{R} \quad \text{or} \quad V = I \cdot R")
        
        resistance = st.slider("Adjust Circuit Resistance (Ohms Ω)", min_value=1, max_value=100, value=10)
        voltage = np.linspace(0, 12, 100)
        current = voltage / resistance
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name=f'R = {resistance} Ω', line=dict(color='#00FFCC', width=3)))
        fig.update_layout(title="Linear I-V Characteristic Curve", xaxis_title="Voltage (V)", yaxis_title="Current (A)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- FEATURE 2: ADVANCED SIGNAL FILTER BODE SIMULATOR ---
    elif "filter" in topic or "rc circuit" in topic:
        st.markdown("### 📡 Subsystem Matrix: RC Low-Pass Filter Frequency Analyzer")
        st.markdown("Mathematical transfer function tracking framework:")
        st.latex(r"H(f) = \frac{1}{1 + j(2\pi f R C)} \quad \Longrightarrow \quad |H(f)| = \frac{1}{\sqrt{1 + (2\pi f R C)^2}}")
        st.latex(r"f_c = \frac{1}{2\pi R C}")
        
        # Live circuit tuning parameter sliders
        r_val = st.slider("Select Resistor Value (Ohms Ω)", min_value=100, max_value=10000, value=1000, step=100)
        c_val_uF = st.slider("Select Capacitor Value (Microfarads μF)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
        
        c_val = c_val_uF * 1e-6  # Convert to Farads
        fc = 1 / (2 * np.pi * r_val * c_val)  # Calculate cutoff frequency
        
        st.metric(label="Calculated Cutoff Frequency (fc)", value=f"{fc:.2f} Hz")
        
        # Frequency spectrum calculations
        frequencies = np.logspace(0, 5, 500)  # 1Hz to 100kHz
        magnitude = 1 / np.sqrt(1 + (2 * np.pi * frequencies * r_val * c_val)**2)
        magnitude_db = 20 * np.log10(magnitude)
        
        # Render Plotly Signal Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=frequencies, y=magnitude_db, mode='lines', name='Magnitude Response', line=dict(color='#FFCC00', width=3)))
        
        # Mark cutoff frequency point visually
        fig.add_vline(x=fc, line_dash="dash", line_color="#FF3366", annotation_text=f"fc ({fc:.1f}Hz)", annotation_position="bottom left")
        
        fig.update_xaxes(type="log")
        fig.update_layout(title="Filter Frequency Response (Bode Amplitude Plot)", xaxis_title="Frequency (Hz, Log Scale)", yaxis_title="Gain (dB)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- FEATURE 3: SEMICONDUCTOR SHOCKLEY DIODE EMULATOR ---
    elif "semiconductor" in topic or "diode" in topic:
        st.markdown("### 🧬 Subsystem Matrix: Diode Shockley Equation")
        st.latex(r"I = I_S \left( e^{\frac{qV}{nkT}} - 1 \right)")
        
        v_diode = np.linspace(-1.0, 0.8, 200)
        Is, Vt = 1e-12, 0.026
        i_diode = Is * (np.exp(v_diode / (1 * Vt)) - 1)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=v_diode, y=i_diode, mode='lines', name='Diode Conduction State', line=dict(color='#FF3366', width=3)))
        fig.update_layout(title="Non-Linear Diode I-V Curve", xaxis_title="Diode Voltage (V)", yaxis_title="Current (A)", yaxis=dict(range=[-1e-9, 0.01]), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)