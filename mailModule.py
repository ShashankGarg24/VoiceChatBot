import botMessagingModule as msg
import audioModule as audio
import smtplib


def send_mails(to, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(keys.EMAIL, keys.PASSWORD)
    server.sendmail('4as1827000224@gmail.com', to, body)
    server.close()


def sendMails():
    try:
        audio.speak("Who do you want to send this mail")
        to = audio.get_audio()
        audio.speak("what should I say to " + to)
        body = audio.get_audio()
        send_mails(keys.DICT[to], body)
        audio.speak("Your mail has been sent successfully !")
        msg.insertMessage("Boss: Your mail has been sent successfully !")
    except Exception as e:
        print(e)
        audio.speak("Sorry, Could not send this E-mail")
        msg.insertMessage("Boss: Sorry, Could not send this E-mail")