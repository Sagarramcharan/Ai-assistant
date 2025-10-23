import os
import pyttsx3
import pyautogui
import webbrowser
import queue
import sounddevice as sd
import vosk
import json

# Initialize speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load the Vosk model
model = vosk.Model("vosk_model")
q = queue.Queue()

# Callback to collect audio input
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Start listening for commands
def start_assistant():
    speak("nova Hello World is now active. What do you want me to do?")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                command = result.get("text", "")
                print("You said:", command)

                # --- TASK EXECUTIONS ---
                if "open notepad" in command:
                    speak("Opening Notepad")
                    os.system("start notepad")

                elif "open youtube" in command:
                    speak("Opening YouTube")
                    webbrowser.open("https://youtube.com")

                elif "type hello world" in command:
                    speak("Typing Hello World")
                    pyautogui.typewrite("Hello World")

                elif "stop Nova" in command or "stop assistant" in command:
                    speak("Goodbye. bad going to sleep.")
                    break

# Main: Wake word detection
def listen_for_wake_word():
    speak("Say 'hey nova' to activate.")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print("Heard:", text)
                if "hey nova" in text:
                    start_assistant()

# Start program
if __name__ == "__main__":
    listen_for_wake_word()
