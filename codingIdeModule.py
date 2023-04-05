import os
import audioModule as audio
import tkinter as tk

def openCodingIDE(a, msg):
    try:
        path = keys.PATH_VS_CODE
        audio.speak(a)
        os.startfile(path)
        msg.insert(tk.END, "Boss: opened visual studio")
    except Exception as e:
        print(e)
        audio.speak("Sorry, Could not open the coding IDE")