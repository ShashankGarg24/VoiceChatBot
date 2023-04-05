import os
import audioModule as audio
import tkinter as tk


def openBrowser(a, msg):
    try:
        path = keys.PATH_BROWSER
        audio.speak(a)
        os.startfile(path)
        msg.insert(tk.END, "Boss: opened browser")
    except Exception as e:
        print(e)
        audio.speak("Sorry, Could not open the browser")

    
