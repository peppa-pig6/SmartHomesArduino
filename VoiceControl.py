import speech_recognition as sr
import serial
import time
import subprocess

# ------------------------
# SETTINGS
# ------------------------

PORT = "/dev/cu.usbmodem12401"
BAUD = 9600

arduino = serial.Serial(PORT, BAUD)
time.sleep(2)

recognizer = sr.Recognizer()

# Better microphone sensitivity
recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 250
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.4

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
    print("Sending:", command)
    arduino.write((command + "\n").encode())

# ------------------------
# EXECUTE COMMAND
# ------------------------

def execute(command):

    command = command.lower()

    print("Recognized:", command)

    # ------------------------
    # ALL LIGHTS
    # ------------------------

    if "all" in command:

        if "off" in command:
            send("all off")
            speak("Turning all lights off.")

        elif "on" in command:
            send("all on")
            speak("Turning all lights on.")

        else:
            speak("Do you want all lights on or off?")

    # ------------------------
    # RED
    # ------------------------

    elif "red" in command:

        if "off" in command:
            send("red off")
            speak("Turning the red light off.")

        elif "on" in command:
            send("red on")
            speak("Turning the red light on.")

        else:
            speak("Do you want the red light on or off?")

    # ------------------------
    # BLUE
    # ------------------------

    elif "blue" in command:

        if "off" in command:
            send("blue off")
            speak("Turning the blue light off.")

        elif "on" in command:
            send("blue on")
            speak("Turning the blue light on.")

        else:
            speak("Do you want the blue light on or off?")

    # ------------------------
    # GREEN
    # ------------------------

    elif "green" in command:

        if "off" in command:
            send("green off")
            speak("Turning the green light off.")

        elif "on" in command:
            send("green on")
            speak("Turning the green light on.")

        else:
            speak("Do you want the green light on or off?")

    # ------------------------
    # HIT IT / SING
    # ------------------------

    elif "hit it" in command or "sing" in command:

        speak("Hit it.")

        # Song code goes here

    # ------------------------
    # UNKNOWN COMMAND
    # ------------------------

    else:
        speak("I don't understand that command.")

# ------------------------
# STARTUP
# ------------------------

speak("Jarvis online.")

# ------------------------
# MAIN LOOP
# ------------------------

while True:

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Waiting for callsign...")

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            text = recognizer.recognize_google(audio).lower()

            print("You:", text)

            if "jarvis" in text:

                speak("Yes sir.")

                print("Listening for command...")

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )

                command = recognizer.recognize_google(audio).lower()

                print("Command:", command)

                execute(command)

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            pass

        except Exception as e:
            print(e)
