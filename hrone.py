import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Configure Gemini API
genai.configure(api_key="api ")

# Initialize Text-to-Speech (TTS) engine
engine = pyttsx3.init()

# Set voice to female
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():  # Tries to find a female voice
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 180)  # Adjusts speech rate for clarity

def text_to_speech(text):
    
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
  
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (or type your message below)")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            print("Could not request results, check your internet.")
            return ""

def get_gemini_response(user_input):
  
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        prompt = f"""You are an HR of office. Your task is to provide clear and concise responses to employee queries. 
        Respond formally, concisely, and in a corporate-friendly manner.
        User Query: {user_input}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return "I apologize, but I encountered an issue."

def hr_assistant():
    
    print("HR Assistant is active. Say 'exit' to stop.")
    
    while True:
        user_input = input("Type your message (or press Enter to speak): ").strip()
        
        if not user_input:  # If no text input, switch to voice mode
            user_input = speech_to_text()
        
        if not user_input:
            continue

        if "exit" in user_input.lower():
            print("Goodbye! Have a great day.")
            text_to_speech("Goodbye! Have a great day.")
            break
        
        response = get_gemini_response(user_input)
        print(f"HR Assistant: {response}")
        text_to_speech(response)

# Run the HR Assistant
if __name__ == "__main__":
    hr_assistant()
