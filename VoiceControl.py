import speech_recognition as sr
import serial
import time
import subprocess

# ------------------------
# SETTINGS
# ------------------------

PORT = "/dev/cu.usbmodem112401"
BAUD = 9600

arduino = serial.Serial(PORT, BAUD)
time.sleep(2)

recognizer = sr.Recognizer()

# ------------------------
# TEXT TO SPEECH
# ------------------------

def speak(text):
    print("Jarvis:", text)
    subprocess.run(["say", text])

# ------------------------
# SEND TO ARDUINO
# ------------------------

def send(command):
    arduino.write((command + "\n").encode())

# ------------------------
# EXECUTE COMMAND
# ------------------------

def execute(command):

    command = command.lower()

    if "green" in command:
        send("green")
        speak("Green light activated.")

    elif "yellow" in command:
        send("yellow")
        speak("Yellow light activated.")

    elif "red" in command:
        send("red")
        speak("Red light activated.")

    else:
        speak("I don't understand that command.")

# ------------------------
# MAIN LOOP
# ------------------------

speak("Jarvis online.")

while True:

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        print("Listening for callsign...")

        audio = recognizer.listen(source)

        try:

            text = recognizer.recognize_google(audio).lower()

            print("You:", text)

            if "jarvis" in text:

                speak("Yes sir.")

                print("Listening for command...")

                audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)

                print("Command:", command)

                execute(command)

        except sr.UnknownValueError:
            pass

        except Exception as e:
            print(e)
