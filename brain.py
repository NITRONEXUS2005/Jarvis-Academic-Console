from study_tracker import (start_study, stop_study, show_progress, show_subject_ranking, generate_suggestions)
from exam_mode import launch_exam_mode
from academic_assistant import (explain_topic, summarize_topic, generate_questions)
from voice import take_voice_command
from study_tracker import generate_ai_suggestions
from study_tracker import resume_last_session

def process_command(command, actions):
    command = command.lower().strip()

    if "google" in command:
        actions.open_google()

    elif "youtube" in command:
        actions.open_youtube()
    
    elif "start study" in command:
        subject = command.replace("start study", "").strip()
        if subject:
            start_study(subject)
            actions.speak(f"Started studying {subject}.")
        else:
            actions.speak("Please specify a subject.")

    elif "stop study" in command:
        stop_study()
        actions.speak("Study session has ended.")  

    elif "show progress" in command:
        show_progress()
        actions.speak("Displaying study progress.")             
    
    elif "subject ranking" in command:
        show_subject_ranking()
        actions.speak("Displaying subject ranking.")

    elif "study suggestion" in command:
        generate_suggestions()
        actions.speak("Generating study suggestion.")    

    elif "exam mode" in command:
        subject = command.replace("exam mode", "").strip()
        if subject:
            # Pass actions.init_driver() to ensure the browser exists, then pass the driver object
            actions.init_driver()
            launch_exam_mode(subject, take_voice_command, actions.speak, actions.driver)
        else:
            actions.speak("Please specify a subject.")    

    elif "play" in command:
        song = command.replace("play", "").strip()
        actions.play_music(song)

    elif "explain" in command:
        topic = command.replace("explain", "").strip()
        if topic:
            actions.speak(f"Explaining {topic}")
            explain_topic(topic, actions.speak)
        else:
            actions.speak("Please specify a topic.")        

    elif "summarize" in command:
        topic = command.replace("summarize", "").strip()
        if topic:
            actions.speak(f"Summarizing {topic}")
            summarize_topic(topic, actions.speak)
        else:
            actions.speak("Please specify a topic.")

    elif "generate questions" in command:
        topic = command.replace("generate questions", "").strip()
        if topic:
            actions.speak(f"Generating revision questions for {topic}")
            generate_questions(topic, actions.speak)
        else:
            actions.speak("Please specify a topic.")      

    elif "help" in command: # FIXED: Was "help in command"
        actions.show_help()        

    elif "ai suggestion" in command:
        generate_ai_suggestions(actions.speak)    

    elif "complete topic" in command:
        topic_details = command.replace("complete topic", "").strip()
        if topic_details:
            from study_tracker import mark_topic_completed_direct
            mark_topic_completed_direct(topic_details, actions)
        else:
            actions.speak("Please specify which topic you want to mark complete.")
                      
    elif "resume study" in command or "track back" in command or "suggest last subject" in command:
        resume_last_session(actions)
    else:
        actions.speak("Command not recognized.")