import os
import audioModule as audio
import botMessagingModule as msg


def openCodingIDE(a):
    try:
        path = keys.PATH_VS_CODE
        audio.speak(a)
        os.startfile(path)
        msg.insertMessage("Boss: opened visual studio")
    catch Exception as e:
        print(e)
        audio.speak("Sorry, Could not open the coding IDE")