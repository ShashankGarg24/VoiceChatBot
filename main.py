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
import keys
import wikipediaModule as wiki
import musicModule as music
import codingIdeModule as codeIde
import browserModule as browser
import audioModule as audio
import makeNote as notes
import googleSearchModule as webSearch
import mailModule as mail
import pyttsx3
import speech_recognition as sr

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
msg_list = tk.Listbox(frame, height=20, width=50, yscrollcommand=y_scroll_bar.set, xscrollcommand=x_scroll_bar.set)
y_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.FALSE)
x_scroll_bar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.FALSE)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
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


prepare_tags_list()


def main():
    sentence = audio.get_audio()
    print(sentence)
    msg_list.insert(tk.END, "You: " + sentence)
    if sentence.count("exit") > 0:
        msg_list.insert(tk.END, "Boss: Good Bye!")
        audio.speak("Good bye")
        root.quit()

    tag = model.predict_tag(sentence)
    sub = sub_tags_models[tag].predict_tag(sentence)
    tag_word = tags[tag]

    sub_list = tags_dict.get(tag_word)
    sub_tag_word = sub_list[sub]

    if sub_tag_word == "mails-send":
        print("mails-send")
        mail.sendMails(msg_list)

    elif sub_tag_word == "wikipedia-open":
        print("wikipedia-open")
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        wiki.runWikipediaSearch(a, msg_list)
        
    elif sub_tag_word == "music-open":
        print("music-open")
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        music.openMusicApp(a, msg_list)

    elif sub_tag_word == "visual-studio-code-open":
        print("visual-studio-code-open")
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        codeIde.openCodingIDE(a, msg_list)

    elif sub_tag_word == "browser-open":
        print("browser-open")
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        browser.openBrowser(a, msg_list)

    elif sub_tag_word == "call-weather-api":
        print("call-weather-api")
        weather.fetchWeatherDetails(msg_list)

    elif sub_tag_word == "know-date":
        print("know-date")
        date = cl.get_date_for_day(sentence)
        audio.speak(date)
        msg_list.insert(tk.END, "Boss: " + str(date))

    elif sub_tag_word == "get-events":
        try:
            print("get-events")
            day = cl.get_date(sentence)
            cl.get_selected_events(SERVICE, day, msg_list)
        except:
            audio.speak("None")
            msg_list.insert(tk.END, "Boss: None")
    elif sub_tag_word == "all-events":
        try:
            print("all-events")
            cl.get_all_events(SERVICE, msg_list)
        except:
            msg_list.insert(tk.END, "Boss: None")
            audio.speak("None")

    elif sub_tag_word == "make-notes":
        print("make-notes")
        notes.make_note(msg_list)

    elif sub_tag_word == "search-google":
        print("search-google")
        webSearch.perform_google_search(msg_list)

    else:
        print("Else")
        ans = answers_dict.get(sub_tag_word)
        a = random.choice(ans)
        audio.speak(a)
        msg_list.insert(tk.END, "Boss: " + str(a))


def run():
    main_thread = threading.Thread(target=main)
    main_thread.start()


picture = tk.PhotoImage(file=keys.PATH_IMAGE)
send_button = tk.Button(root, image=picture, command=run, borderwidth=0)
send_button.pack()

wish()

root.mainloop()
