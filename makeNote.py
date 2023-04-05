import datetime
import subprocess


def note(text):
    date = datetime.datetime.now()
    file_name = "notes/" + str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def make_note():
    audio.speak("What would you like me to write down? ")
    write = audio.get_audio()
    note(write)
    audio.speak("I've made a note of that.")
    msg_list.insert(tk.END, "Boss: I've made a note of that.")