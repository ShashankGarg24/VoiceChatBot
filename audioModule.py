import pyttsx3
import speech_recognition as sr


def speak(text):
    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said