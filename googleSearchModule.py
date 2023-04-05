import botMessagingModule as msg
import webbrowser as wb
import audioModule as audio
try:
    from googlesearch import search
except:
    print("googlesearch not imported!")


def perform_google_search():
    audio.speak("what would you like me to search for")
    query = audio.get_audio()
    audio.speak("I have the following results")
    msg.insertMessage("Boss: I have the following results:")
    for result in search(query, tld="co.in", num=1, stop=1, pause=2):
        msg.insertMessage("Boss: " + str(result))
        res = result

    wb.open(res)