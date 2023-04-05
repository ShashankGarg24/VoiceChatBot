import wikipedia as wiki
import audioModule as audio
import botMessagingModule as msg

def runWikipediaSearch(a):
    try:
        audio.speak("What you want to search for?")
        searchFor = audio.get_audio()
        print("searchFor: " + str(searchFor))
        audio.speak(a)
        results = wiki.summary(str(searchFor), auto_suggest=False, sentences=3)
        audio.speak("According to wikipedia")
        print(results)
        audio.speak(results)
        msg.insertMessage("Boss: " + str(results))
    catch Exception as e:
        print(e)
        audio.speak("Cannot open wikipedia results")