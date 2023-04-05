import tkinter as tk
import webbrowser as wb
import audioModule as audio
try:
    from googlesearch import search
except:
    print("googlesearch not imported!")


def perform_google_search(msg):
    try:
        audio.speak("what would you like me to search for")
        query = audio.get_audio()
        audio.speak("I have the following results")
        msg.insert(tk.END, "Boss: I have the following results:")
        for result in search(query, tld="co.in", num=1, stop=1, pause=2):
            msg.insert(tk.END, "Boss: " + str(result))
            res = result

        wb.open(res)

    except:
        msg.insert(tk.END, "Boss: An error occurred!")
        audio.speak("An error occurred")
