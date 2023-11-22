from gtts import gTTS
import os
import pygame
import speech_recognition as sr
import datetime
import psutil
import webbrowser
import time
import subprocess
import wolframalpha
from ytmusicapi import YTMusic
import pyautogui
import keyFile
import openai
import weather
import requests


class Shabnam:
    def __init__(self):
        pygame.init()
        self.engine = None
        self.recognizer = sr.Recognizer()
        self.wolfram_alpha_app_id = (
            keyFile.WOLFRAM
        )  # Replace with your Wolfram Alpha app ID
        self.ytmusic = YTMusic("oauth.json")
        self.openai_api_key = keyFile.OPENAI  # Replace with your OpenAI API key
        openai.api_key = self.openai_api_key
        self.weather_api_key = (
            keyFile.WEATHER_API
        )  # Replace with your OpenWeatherMap API key

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening for wake word...")
            try:
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                if "shabnam" in command:
                    self.detected_callback()
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )

    def detected_callback(self):
        while True:
            with sr.Microphone() as source:
                print("Listening for command...")
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    print("You said:", command)
                    if "hello" in command or "hi" in command:
                        self.talk("Hi there! How can I help you?")
                    elif "goodbye" in command or "bye" in command:
                        self.talk("Goodbye! Have a great day!")
                        exit()
                    elif "time" in command:
                        current_time = datetime.datetime.now().strftime("%H:%M")
                        self.talk(f"The current time is {current_time}")
                    elif "battery" in command:
                        battery_percentage = psutil.sensors_battery().percent
                        self.talk(f"The battery is at {battery_percentage}%")
                    elif "open google" in command:
                        self.talk("Sure, opening Google.")
                        webbrowser.open("https://www.google.com")
                    elif "open youtube" in command:
                        self.talk("Sure, opening YouTube.")
                        webbrowser.open("https://www.youtube.com")
                    elif "system information" in command:
                        self.system_information()
                    elif "search" in command:
                        search_query = command.replace("search", "").strip()
                        self.search_information(search_query)
                    elif "calculate" in command or "math" in command:
                        math_query = (
                            command.replace("calculate", "").replace("math", "").strip()
                        )
                        self.calculate_math(math_query)
                    elif "open whatsapp" in command:
                        self.talk("Sure, opening WhatsApp.")
                        subprocess.run(["open", "-a", "WhatsApp"])
                    elif "open telegram" in command:
                        self.talk("Sure, opening Telegram.")
                        subprocess.run(["open", "-a", "Telegram"])
                    elif "open vscode" in command:
                        self.talk("Sure, opening VS Code.")
                        subprocess.run(["open", "-a", "Visual Studio Code"])
                    elif "open spotify" in command:
                        self.talk("Sure, opening Spotify.")
                        subprocess.run(["open", "-a", "Spotify"])
                    elif "open terminal" in command:
                        self.talk("Sure, opening Terminal.")
                        subprocess.run(["open", "-a", "Terminal"])
                    elif "open finder" in command:
                        self.talk("Sure, opening Finder.")
                        subprocess.run(["open", "-a", "Finder"])
                    elif "open app store" in command:
                        self.talk("Sure, opening App Store.")
                        subprocess.run(["open", "-a", "App Store"])
                    elif "open chrome" in command:
                        self.talk("Sure, opening Chrome.")
                        subprocess.run(["open", "-a", "Google Chrome"])
                    elif "open notes" in command or "open notes" in command:
                        self.talk("Sure, opening Notes.")
                        subprocess.run(["open", "-a", "Notes"])
                    elif "open calendar" in command or "show calendar" in command:
                        self.talk("Sure, opening Calendar.")
                        subprocess.run(["open", "-a", "Calendar"])

                    elif "open website" in command:
                        website = (
                            command.replace("open website", "")
                            .strip()
                            .replace(" ", "")
                            .replace("dot", ".")
                            .strip()
                        )
                        self.talk(f"Sure, opening {website}.")
                        webbrowser.open(f"https://{website}")
                    elif "play music" in command:
                        self.play_music()
                    elif "play replay mix" in command or "play replay" in command:
                        self.talk("Sure, playing replay mix.")
                        webbrowser.open(keyFile.REPLAY_PLAYLIST)
                        time.sleep(3)
                        pyautogui.press("space")
                    elif "tell me a joke" in command:
                        joke = self.get_joke()
                        self.talk(joke)
                    elif "what's the weather at" in command:
                        location = command.replace("what's the weather at", "").strip()
                        print(location)
                        self.get_weather_at(location)

                    elif "weather" in command:
                        self.get_weather()
                    else:
                        self.talk(
                            "Sorry, I didn't understand that. Can you please repeat?"
                        )
                except sr.WaitTimeoutError:
                    print("Timed out waiting for command")
                    break
                except sr.UnknownValueError:
                    break
                except sr.RequestError as e:
                    print(
                        f"Could not request results from Google Speech Recognition service; {e}"
                    )

    def talk(self, text):
        print(text)
        tts = gTTS(text=text, lang="en")
        tts.save("temp.mp3")
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove("temp.mp3")

    def system_information(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent
        self.talk(
            f"CPU usage is {cpu_usage} percent. RAM usage is {ram_usage} percent. Disk usage is {disk_usage} percent."
        )

    def search_information(self, query):
        self.talk(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def calculate_math(self, query):
        try:
            client = wolframalpha.Client(self.wolfram_alpha_app_id)
            res = client.query(query)
            answer = next(res.results).text
            self.talk(f"The answer is {answer}")
        except Exception as e:
            print(f"Error calculating math: {e}")
            self.talk("Sorry, I couldn't perform the calculation.")

    def play_music(self):
        try:
            playlists = self.ytmusic.get_library_playlists()
            if playlists:
                playlist_id = playlists[0]["playlistId"]
                playlist_url = f"https://music.youtube.com/playlist?list={playlist_id}"
                self.talk("Sure, playing music.")
                webbrowser.open(playlist_url)
                time.sleep(3)  # Wait for the page to load
                pyautogui.press("space")
            else:
                self.talk(
                    "Sorry, I couldn't find any playlists in your YouTube Music library."
                )
        except Exception as e:
            print(f"Error playing music: {e}")
            self.talk("Sorry, I couldn't play music at the moment.")

    def get_joke(self):
        response = openai.Completion.create(
            engine="davinci",
            prompt="Tell me a joke:",
            max_tokens=50,
        )
        joke = response.choices[0].text.strip()
        return joke

    def get_weather(self):
        location = "chennai"  # Replace with the desired city
        try:
            current_weather = weather.get_weather(location, self.weather_api_key)
            current_weather = current_weather.split("-")
            temperature = current_weather[1]
            description = current_weather[2]
            self.talk(
                f"The current weather in {location} is {temperature} with {description}."
            )
        except Exception as e:
            print(f"Error fetching weather information: {e}")
            self.talk("Sorry, I couldn't fetch the weather information.")

    def get_weather_at(self, location):
        location = location  # Replace with the desired city
        try:
            current_weather = weather.get_weather(location, self.weather_api_key)
            current_weather = current_weather.split("-")
            temperature = current_weather[1]
            description = current_weather[2]
            self.talk(
                f"The current weather in {location} is {temperature} with {description}."
            )
        except Exception as e:
            print(f"Error fetching weather information: {e}")
            self.talk("Sorry, I couldn't fetch the weather information.")


shabnam = Shabnam()

with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    shabnam.recognizer.adjust_for_ambient_noise(source, duration=5)

print("Shabnam is ready. Say 'Shabnam' to start.")

try:
    while True:
        shabnam.take_command()
        time.sleep(2)
except KeyboardInterrupt:
    print("Shutting down...")
