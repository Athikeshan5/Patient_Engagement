import speech_recognition as sr

# Initialize recognizer class (for recognizing speech)
recognizer = sr.Recognizer()

def voice_to_text():
    # Loop to continuously listen to the microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust to ambient noise for better accuracy
        print("Listening for speech...")

        while True:
            try:
                # Capture the audio from the microphone
                audio_data = recognizer.listen(source)
                print("Recognizing...")

                # Convert speech to text using Google Speech Recognition
                text = recognizer.recognize_google(audio_data)
                
                # Display the recognized text
                print(f"Recognized Text: {text}")

            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    voice_to_text()
