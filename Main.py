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


class Shabnam:
    def __init__(self):
        pygame.init()
        self.engine = None
        self.recognizer = sr.Recognizer()
        self.wolfram_alpha_app_id = (
            keyFile.WOLFRAM  # Replace with your Wolfram Alpha app ID
        )
        self.ytmusic = YTMusic("oauth.json")

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
                    if (
                        "hello" in command
                        or "hi" in command
                        or "hey" in command
                        or "yo" in command
                        or "sup" in command
                    ):
                        self.talk("Hi there! How can I help you?")
                    elif (
                        "goodbye" in command
                        or "bye" in command
                        or "exit" in command
                        or "quit" in command
                        or "stop" in command
                        or "shut down" in command
                        or "shutup" in command
                        or "shut up" in command
                    ):
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
                    elif (
                        "play replay mix" in command
                        or "play replay" in command
                        or "play my mix" in command
                        or "play my replay mix" in command
                        or "play my replay" in command
                        or "play replay playlist" in command
                        or "play replay mix playlist" in command
                    ):
                        self.talk("Sure, playing replay mix.")
                        webbrowser.open(keyFile.REPLAY_PLAYLIST)
                        time.sleep(3)
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
