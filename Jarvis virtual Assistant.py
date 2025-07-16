import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
import pygame
from gtts import gTTS
import os


# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "2be341cf3b52485a91c5067e6a33c125"  # Your NewsAPI key

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
        api_key="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"  # Replace with your actual key
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis for general tasks like Alexa and Google Assistant."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    c_lower = c.lower()
    
    if "open google" in c_lower:
        webbrowser.open("https://google.com")
    elif "open facebook" in c_lower:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c_lower:
        webbrowser.open("https://youtube.com")
    elif c_lower.startswith("play"):
        try:
            song = c_lower.split(" ", 1)[1]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak(f"Sorry, I don't have the song {song} in my library.")
        except IndexError:
            speak("Please specify a song to play.")
    elif "news" in c_lower:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            if articles:
                for article in articles[:5]:  # Limit to top 5 headlines
                    speak(article['title'])
            else:
                speak("I couldn't find any news articles.")
        else:
            output = aiProcess(c)
            speak(output)
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("Recognizing....")
        try:
            with sr.Microphone() as source:
                print(" Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Yes sir?")
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
 
                        processCommand(command)

         
        except Exception as e:
            print(f"Error: {e}")
