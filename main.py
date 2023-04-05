import numpy as np
import json
from model import create_model
import random
import tensorflow as tf
from prepare import prepare_data
import calender as cl
import subprocess
import datetime
import tkinter as tk
import os
import threading
import weather
import smtplib
import keys
import wikipediaModule as wiki
import musicModule as music
import codingIdeModule as codeIde
import browserModule as browser
import audioModule as audio
import botMessagingModule as msg
import makeNote as notes
import googleSearchModule as webSearch


SERVICE = cl.authenticate()

root = tk.Tk()
root.geometry('500x600')
heading = tk.Label(root, text="Welcome! Press the Button and ask whatever you want!",
                   font=('montserrat', 12, "bold"), fg="black").pack()
frame = tk.Frame(root, bg="#FFF")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
your_msg = tk.StringVar()
y_scroll_bar = tk.Scrollbar(frame)
x_scroll_bar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
y_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.FALSE)
x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.FALSE)
createMessageListBox(frame, y_scroll_bar, x_scroll_bar)
frame.pack()

with open("intents.json") as file:
    data = json.load(file)



tags = []  # Contains all the different tags
all_questions_list = []  # Contains the different question with their words tokenized
questions_tags = []  # Contains the questions tags corresponding to the questions in above list
all_question_words = []  # Contains all the words in all the questions of the dataset

pr = prepare_data(data)
all_question_words, tags, all_questions_list, questions_tags = pr.prepare(data, "intents", "all_questions", "tag")

all_questions_train = []
tags_output = []

all_questions_train, tags_output = pr.get_training_set()
all_questions_train = np.array(all_questions_train)
tags_output = np.array(tags_output)

tf.compat.v1.reset_default_graph()
model = create_model(all_questions_train, tags_output, tags, all_question_words)
model.fit_model(all_questions_train, tags_output)

# Preparing sub tags models
sub_tags_list = []
sub_tags_models = []

for intent in data["intents"]:
    all_words_sub_questions = []
    all_sub_tags = []
    sub_question_tags = []
    all_sub_questions_list = []

    tr = prepare_data(data)
    all_words_sub_questions, all_sub_tags, all_sub_questions_list, sub_question_tags = tr.prepare(intent, "sub_tags",
                                                                                                  "questions", "sub")

    all_sub_questions_train = []
    sub_tags_output = []
    all_sub_questions_train, sub_tags_output = tr.get_training_set()
    all_sub_questions_train = np.array(all_sub_questions_train)
    sub_tags_output = np.array(sub_tags_output)

    sub_model = create_model(all_sub_questions_train, sub_tags_output, all_sub_tags, all_words_sub_questions)
    sub_model.fit_model(all_sub_questions_train, sub_tags_output)
    sub_tags_models.append(sub_model)

    sub_tags_list.extend(all_sub_tags)

tags_dict = {}
answers_dict = {}


def prepare_tags_list():
    for intent in data["intents"]:
        curr_tag = intent["tag"]
        s_tags_list = []
        for sub_tg in intent["sub_tags"]:
            curr_sub_tag = sub_tg["sub"]
            s_tags_list.append(curr_sub_tag)
            answers_dict[curr_sub_tag] = sub_tg["answers"]

        tags_dict[curr_tag] = s_tags_list


def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        audio.speak("Good Morning")
    elif 12 <= hour < 18:
        audio.speak("Good Afternoon")
    else:
        audio.speak("Good Evening")
    audio.speak("I am Boss sir, How can I help you")




def send_mails(to, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(keys.EMAIL, keys.PASSWORD)
    server.sendmail('4as1827000224@gmail.com', to, body)
    server.close()


prepare_tags_list()


def main():
    sentence = audio.get_audio()
    msg.insertMessage("You: " + sentence)
    if sentence.count("exit") > 0:
        msg.insertMessage("Boss: Good Bye!")
        audio.speak("Good bye")
        root.quit()

    tag = model.predict_tag(sentence)
    sub = sub_tags_models[tag].predict_tag(sentence)
    tag_word = tags[tag]

    sub_list = tags_dict.get(tag_word)
    sub_tag_word = sub_list[sub]

    if sub_tag_word == "mails-send":
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
    elif sub_tag_word == "wikipedia-open":
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        wiki.runWikipediaSearch(a)
        
    elif sub_tag_word == "music-open":
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        music.openMusicApp(a)

    elif sub_tag_word == "visual-studio-code-open":
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        codeIde.openCodingIDE(a)

    elif sub_tag_word == "browser-open":
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        browser.openBrowser(a)

    elif sub_tag_word == "call-weather-api":
        weather.fetchWeatherDetails()

    elif sub_tag_word == "know-date":
        date = cl.get_date_for_day(sentence)
        audio.speak(date)
        msg.insertMessage("Boss: " + str(date))

    elif sub_tag_word == "get-events":
        try:
            day = cl.get_date(sentence)
            cl.get_selected_events(SERVICE, day, tk)
        except:
            audio.speak("None")
            msg.insertMessage("Boss: None")
    elif sub_tag_word == "all-events":
        try:
            cl.get_all_events(SERVICE, tk)
        except:
            msg.insertMessage("Boss: None")
            audio.speak("None")

    elif sub_tag_word == "make-notes":
        try:
            notes.make_note()
        except:
            msg.insertMessage("Boss: Try again")
            audio.speak("try again")
    elif sub_tag_word == "search-google":
        try:
            webSearch.perform_google_search()
        except:
            msg.insertMessage("Boss: An error occurred!")
            audio.speak("An error occurred")
    else:
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        audio.speak(a)
        msg.insertMessage("Boss: " + str(a))


def run():
    main_thread = threading.Thread(target=main)
    main_thread.start()


picture = tk.PhotoImage(file=keys.PATH_IMAGE)
send_button = tk.Button(root, image=picture, command=run, borderwidth=0)
send_button.pack()

wish()

root.mainloop()
