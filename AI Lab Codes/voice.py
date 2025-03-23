import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to recognize speech
def recognize_speech():
    # Use the default microphone for audio input
    with sr.Microphone() as source:
        print("Say something...")
        
        # Adjust for ambient noise and listen to the microphone
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize the speech using Google Web Speech API
        print("Recognizing...")
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")

        # Respond with text-to-speech
        engine.say(f"You said: {speech_text}")
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        engine.say("Sorry, I could not understand the audio.")
        engine.runAndWait()
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        engine.say("Could not request results from Google Speech Recognition service.")
        engine.runAndWait()

# Run the voice recognition
if __name__ == "__main__":
    recognize_speech()
