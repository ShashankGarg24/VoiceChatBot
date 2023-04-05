import os
import audioModule as audio
import botMessagingModule as msg


def openMusicApp(a):
    try:
        path = keys.PATH_MUSIC
        audio.speak(a)
        os.startfile(path)
        msg.insertMessage("Boss: opened Music")
    catch Exception as e:
        print(e)
        audio.speak("Sorry, Could not open the music app")
    