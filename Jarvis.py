import pyttsx3
import os
import urllib.request
import re
import random
from datetime import date, datetime
import speech_recognition as sr
import wikipedia
import webbrowser
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

music_words = ['music','song','songs']

quit_words = ['can go','quit',"you may go","you can go",
                "goodbye","bye","going","leaving","go away",
                "go now","leave","get lost"]

intro_words = ['tell about yourself','give me an intro','who are you',
                'what can you do','tell about you','please introduce yourself',
                'introduction of yourself','tell everyone about you','tell me about you']

calling_words = ['jarvis', 'hello', 'are you there',
                'hey', 'are you listening', 'can you']

def speak(audio):
        # takes a text and speaks it

        engine.say(audio)
        engine.runAndWait()

        

def doIntro():
    speak("I am Jarvis! I am your Laptop buddy!")
    speak("I can help you with things around here")
    speak("I can open websites for you, play songs from your music folder")
    speak("Or Maybe.. You can ask me to play something in youtube")
    speak("Or.. You can ask me to wait and i will wait till you call me again")
    
def open_YTVideo(name):
    if name[0]==' ':
        name = name[1:]
    if name[len(name)-1] == ' ':
        name = name[:len(name)-2]
        
    name = name.replace(" ","+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+name)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]
    webbrowser.get('chrome').open(url)




def wishMe():
    # wishes based on time and introduces himself

    hour = int(datetime.now().hour)

    speak("Helloo Sir! ")

    if 0<=hour<12:
        speak("Good morning!")
    elif 12<=hour<18:
        speak("Good afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis! I am your Laptop buddy!")
    

def waitTillCall():
    speak("ok Sir.. I will wait until you call my name...")
    query = 'waiting'
    name = 'jarvis'
    while any([n for n in calling_words if n in query])==False:
        print(query)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
        except Exception as e:
            pass
        query = query.lower()
    return True


def takeCommand():
    # takes a mic input from user and returns str
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("How can I help you ?")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        # speak("Recognising...")
        query = r.recognize_google(audio, language='en-in')
        # speak(f"you said: {query}\n")
    
    except Exception as e:
        speak("Say that again please..?")
        return "None"
    
    return query

def useQuery(query):
    if any([n for n in intro_words if n in query]):
        doIntro()
        return waitTillCall()

    elif 'search' in query and 'wikipedia' in query:
        speak("Searching wikipedia...")
        query = query.replace("search wikipedia for","")
        results = wikipedia.summary(query,sentences=2)
        print(results)
        speak(results)
        return waitTillCall()

    elif 'play' in query and 'in youtube' in query:
        query = query.replace("play","")
        query = query.replace("in youtube","")
        name = query
        open_YTVideo(name)
        return waitTillCall()

    elif 'open' in query and 'chrome' in query:
        query = query.replace("open","")
        query = query.replace("in chrome","")
        query = query.replace(" ","")
        webbrowser.get('chrome').open(query)
        return waitTillCall()

    elif 'play' in query and any([n for n in music_words if n in query]):
        music_dir = 'D://pics_and_songs//nav_musiq//'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir,songs[random.randint(0,len(songs)-1)]))
        return waitTillCall()

    elif 'time' in query and 'what' in query:
        strTime = datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
        return True
    
    elif any([n for n in quit_words if n in query]):
        speak("Ok sir, thank you. bye then..")
        return False

    elif 'wait' in query:
        return waitTillCall()

    else:
        speak("I am going now... bye then")
        return False



