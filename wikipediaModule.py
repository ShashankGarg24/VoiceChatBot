import wikipedia as wiki
import audioModule as audio
import tkinter as tk

def runWikipediaSearch(a, msg):
    try:
        audio.speak("What you want to search for?")
        searchFor = audio.get_audio()
        print("searchFor: " + str(searchFor))
        audio.speak(a)
        results = wiki.summary(str(searchFor), auto_suggest=False, sentences=3)
        audio.speak("According to wikipedia")
        print(results)
        audio.speak(results)
        msg.insert(tk.END, "Boss: " + str(results))
    except Exception as e:
        print(e)
        audio.speak("Cannot open wikipedia results")