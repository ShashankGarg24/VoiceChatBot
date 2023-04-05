import os
import audioModule as audio
import botMessagingModule as msg


def openBrowser(a):
    try:
        path = keys.PATH_BROWSER
        audio.speak(a)
        os.startfile(path)
        msg.insertMessage("Boss: opened browser")
    catch Exception as e:
        print(e)
        audio.speak("Sorry, Could not open the browser")

    
