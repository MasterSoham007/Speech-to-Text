import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import os, subprocess

# Voice / Language options
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id3 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id4 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id5 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'

r = sr.Recognizer()
# hear the microphone and return the audio as text
def transform_audio_into_text():

    # store recognizer in variable
    r = sr.Recognizer()


    with sr.Microphone() as source:

        # waiting time
        r.pause_threshold = 0.8

        # report that recording has begun
        print("You can now speak")

        # save what you hear as audio
        audio = r.listen(source)

        try:
            # search on google
            request = r.recognize_google(audio, language="en-gb")

            # test in text
            print("You said " + request)

            # return request
            return request

        # In case it doesn't understand audio
        except sr.UnknownValueError:

            print("Ups! I didn't understand audio")
            return "I am still waiting"

        # In case the request cannot be resolved
        except sr.RequestError:

            print("Ups! there is no service")
            return "I am still waiting"

        except:

            print("Ups! something went wrong")

            # return error
            return "I am still waiting"


def speak(message):

    engine = pyttsx3.init()
    engine.setProperty('voice', id3)

    engine.say(message)
    engine.runAndWait()


def ask_day():

    day = datetime.date.today()
    print(day)

    week_day = day.weekday()
    print(week_day)

    # Names of days
    calendar = {0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'}

    speak(f'Today is {calendar[week_day]}')


def ask_time():

    time = datetime.datetime.now()
    time = f'At this moment it is {time.hour} hours and {time.minute} minutes'
    print(time)
    speak(time)


# Create initial greeting
def initial_greeting():
    speak('Hello I am Hazel. How can I help you?')

def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
    except FileNotFoundError:
        print("Notepad not found on your system.")

def open_vscode():
    try:
        vscode_path = r'C:\Users\Asus\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        subprocess.Popen([vscode_path])
    except FileNotFoundError:
        print("Visual Studio Code not found on your system.")

def open_folder(folder_name):
    # Define the base directory where you want to search
    base_dir = "C://Users//Asus//AppData//Roaming//Microsoft//Windows//Start Menu//Programs"

    # Walk through the directory structure to find the folder
    for root, dirs, files in os.walk(base_dir):
        if folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            os.system(f'xdg-open "{folder_path}"')  # Open folder using default file manager
            return
    print("Folder not found.")

def my_assistant():
    initial_greeting()
    go_on = True

    while go_on:
        # Activate microphone and save request
        my_request = transform_audio_into_text().lower()

        if 'open youtube' in my_request:
            speak('Opening youtube')
            webbrowser.open('https://www.youtube.com')
            continue

        elif 'open lead code' in my_request:
            speak('Open leetcode')
            webbrowser.open('https://leetcode.com/anikpal12672/')
            continue

        elif 'open browser' in my_request:
            speak('Of course, I am on it')
            webbrowser.open('https://www.google.com')
            continue

        elif 'what day is today' in my_request:
            ask_day()
            continue

        elif 'what time it is' in my_request:
            ask_time()
            continue

        elif 'do a wikipedia search for' in my_request:
            speak('I am looking for it')
            my_request = my_request.replace('do a wikipedia search for', '')
            answer = wikipedia.summary(my_request, sentences=1)
            speak('according to wikipedia: ')
            speak(answer)
            continue

        elif 'search the internet for' in my_request:
            speak('of course, right now')
            my_request = my_request.replace('search the internet for', '')
            pywhatkit.search(my_request)
            speak('this is what i found')
            continue

        elif 'play' in my_request:
            speak('oh, what a great idea! I´ll play it right now')
            pywhatkit.playonyt(my_request)
            continue

        elif 'joke' in my_request:
            speak(pyjokes.get_joke())
            continue

        elif 'open vs code' in my_request:
            speak('I am opening VS Code')
            open_vscode()
            continue

        elif 'open notepad' in my_request:
            speak('I am opening notepad')
            open_notepad()

        elif 'open vs code' in my_request:
            speak('I am opening vs code')
            open_vscode()

        elif 'stock price' in my_request:
            share = my_request.split()[-2].strip()
            portfolio = {'apple': 'AAPL',
                         'amazon': 'AMZN',
                         'google': 'GOOGL'}
            try:
                searched_stock = portfolio[share]
                searched_stock = yf.Ticker(searched_stock)
                price = searched_stock.info['regularMarketPrice']
                speak(f'I found it! The price of {share} is {price}')
                continue
            except:
                speak('I am sorry, but I didn´t find it')
                continue
        elif 'goodbye' in my_request:
            speak('I am going to rest. Let me know if you need anything')
            break

my_assistant()
