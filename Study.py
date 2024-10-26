import speech_recognition as sr
import difflib

def get_text_input():
    text = input("Enter the text for the user to repeat: ")
    return text

def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak the text you just entered...")
        audio = recognizer.listen(source)
        try:
            spoken_text = recognizer.recognize_google(audio)
            print("You said:", spoken_text)
            return spoken_text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Error with the speech recognition service.")
    return ""
#--^^ best


def compare_texts(original_text, spoken_text):
    original_words = original_text.split()
    spoken_words = spoken_text.split()
    diff = difflib.ndiff(original_words, spoken_words)
    
    differences = [word for word in diff if word[0] != ' ']
    
    if not differences:
        print("Perfect match!")
    else:
        print("Differences found:")
        for difference in differences:
            if difference.startswith('-'):
                print(f"Missing word: {difference[2:]}")
            elif difference.startswith('+'):
                print(f"Extra word: {difference[2:]}")
            else:
                print(f"Changed word: {difference[2:]}")


original_text = get_text_input()
spoken_text = listen_and_recognize()

if spoken_text:
    compare_texts(original_text, spoken_text)
