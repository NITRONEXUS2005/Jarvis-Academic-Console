from voice import take_voice_command, speak
import brain
import actions

actions.set_voice(speak)

print("Jarvis is running...")

while True:
    speak("Say Jarvis to activate")

    wake = take_voice_command()

    if "jarvis" in wake:
        speak("Yes, I'm listening")

        command = take_voice_command()

        if command:
            if "shutdown" in command:
                speak("Goodbye")
                break
            
            brain.process_command(command,actions)