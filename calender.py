from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz
import pyttsx3
import speech_recognition as sr
from pathlib import Path
import httplib2
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import keys

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "febraury", "march", "april", "may", "june", "july", "august", "september"
    , "october", "november", "december"]
DAYS = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
DAY_EXTENTIONS = ["st", "nd", "th", "rd"]
MONTH_DAYS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
              7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
APPLICATION_NAME = 'Boss Chat Bot'
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

    
def speak(text):
    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said


def get_date(text):
    today = datetime.date.today()
    text = text.lower()
    if text.count("today") > 0:
        return today

    if text.count("tomorrow") > 0:
        day = today.day + 1
        if day > MONTH_DAYS.get(today.month):
            day -= MONTH_DAYS.get(today.month)
        month = today.month
        year = today.year
        if month > 11:
            month -= 11
            year += 1

        return datetime.date(month=month, day=day, year=year)

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:
        return datetime.date(month=month, day=day, year=year)


def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

    # Call the Calendar API


def get_event_details(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    start_date = str(start.split("T")[0])
    start_time = str(start.split("T")[1].split("+")[0])
    startDT = datetime.datetime.strptime(start_date + " " + start_time, "%Y-%m-%d %H:%M:%S")
    startDateTime = startDT.strftime("%A, %d %B %Y, %I:%M%p")

    end = event['end'].get('dateTime', event['end'].get('date'))
    end_date = str(end.split("T")[0])
    end_time = str(end.split("T")[1].split("+")[0])
    endDT = datetime.datetime.strptime(end_date + " " + end_time, "%Y-%m-%d %H:%M:%S")
    endDateTime = endDT.strftime("%A, %d %B %Y, %I:%M%p")

    eventText = event["summary"] + " starting at " + startDateTime + " and ending at " + endDateTime
    return eventText


def get_all_events(service, msg_list, tk):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(now)
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=20, singleEvents=True,
                                          orderBy='startTime').execute()
    print(events_result)
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        msg_list.insert(tk.END, "Boss: No upcoming events found!")

    msg_list.insert(tk.END, "Boss: You have " + str(len(events)) + " events")
    speak(f"You have {len(events)} events.")
    for event in events:
        print(event)
        eventText = get_event_details(event)
        print(eventText)
        msg_list.insert(tk.END, "Boss: " + eventText)
        speak(eventText)


def get_selected_events(service, date, msg_list, tk):
    try:
        dtArray = str(date).split("-")
        dt = datetime.date(int(dtArray[0]), int(dtArray[1]), int(dtArray[2]))
        date = datetime.datetime.combine(dt, datetime.datetime.min.time())
        print(date)
        end_date = datetime.datetime.combine(dt, datetime.datetime.max.time())
        utc = pytz.UTC
        date = date.astimezone(utc)
        end_date = end_date.astimezone(utc)

        print(end_date)
        events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                            singleEvents=True, orderBy='startTime').execute()
        print(events_result)
    except Exception as e:
        print(e)
    events = events_result.get('items', [])

    if not events:
        speak('No events found!')
        msg_list.insert(tk.END, "Boss: No events found!")
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            eventText = get_event_details(event)

            msg_list.insert(tk.END, "Boss: " + eventText)
            speak(eventText)


def get_date_for_day(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    if text.count("tomorrow") > 0:
        day = today.day + 1
        month = today.month
        year = today.year
        if day > MONTH_DAYS.get(today.month):
            day -= MONTH_DAYS.get(today.month)
            month += 1

        if month > 11:
            month -= 11
            year += 1

        return datetime.date(month=month, day=day, year=year)

    for word in text.split():
        if word in DAYS:
            # TODO just get the date
            required_day = DAYS.index(word)
            diff = required_day - today.day + 1
            if diff < 0:
                diff += 7
                if text.count("next") >= 1:
                    diff += 7

            curr_month = today.month
            day = today.day + diff
            if day > MONTH_DAYS.get(curr_month):
                day -= MONTH_DAYS.get(curr_month)
                curr_month = today.month - 1
            year = today.year
            return datetime.date(month=curr_month, day=day, year=year)
