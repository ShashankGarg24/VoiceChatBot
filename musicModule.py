import os
import audioModule as audio
import tkinter as tk


def openMusicApp(a, msg):
    try:
        path = keys.PATH_MUSIC
        audio.speak(a)
        os.startfile(path)
        msg.insert(tk.END, "Boss: opened Music")
    except Exception as e:
        print(e)
        audio.speak("Sorry, Could not open the music app")
    