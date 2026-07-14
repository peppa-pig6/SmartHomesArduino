import speech_recognition as sr
import serial
import time
import subprocess

# ------------------------
# SETTINGS
# ------------------------

PORT = "/dev/cu.usbmodem112401"
BAUD = 9600

# Initialize Serial Connection
try:
    arduino = serial.Serial(PORT, BAUD)
    time.sleep(2)
except Exception as e:
    print(f"Error connecting to Arduino on {PORT}: {e}")

recognizer = sr.Recognizer()

# Sensitivity settings
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
    if 'arduino' in globals() and arduino.is_open:
        arduino.write((command + "\n").encode())

# ------------------------
# EXECUTE COMMAND
# ------------------------

def execute(command):
    command = command.lower()

    # Normalize common speech recognition mishearings for "blue"
    if "blew" in command or "blow" in command:
        command = command.replace("blew", "blue").replace("blow", "blue")

    # Exit / Sleep command
    if "go to sleep" in command or "stop listening" in command or "goodbye" in command:
        speak("Going to sleep.")
        return False  # Signals to exit active listening mode

    # ------------------------
    # ALL LIGHTS
    # ------------------------
    if "all" in command:
        if "off" in command:
            send("all off")
            speak("Turning all lights off.")
        elif "on" in command or "one" in command:
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
        elif "on" in command or "one" in command:
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
        elif "on" in command or "one" in command:
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
        elif "on" in command or "one" in command:
            send("green on")
            speak("Turning the green light on.")
        else:
            speak("Do you want the green light on or off?")

    # ------------------------
    # HIT IT / SING
    # ------------------------
    elif "hit it" in command or "sing" in command:
        speak("Hit it.")

    # ------------------------
    # UNKNOWN COMMAND
    # ------------------------
    else:
        speak("I don't understand that command.")

    return True  # Keep active listening mode going

# ------------------------
# STARTUP
# ------------------------

speak("Initiating server connection...")
time.sleep(2)
speak("Jarvis Online")

# ------------------------
# MAIN LOOP
# ------------------------

is_active = False

while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        if not is_active:
            print("Waiting for callsign ('Jarvis')...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                text = recognizer.recognize_google(audio).lower()
                print("You:", text)

                if "jarvis" in text:
                    speak("Yes sir?")
                    is_active = True

            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except Exception as e:
                print("Error:", e)

        # Active Mode: Listens continuously without needing "Jarvis" again
        else:
            print("Listening for commands continuously...")
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()
                print("Command:", command)

                # Execute command; returns False if you told him to go to sleep
                is_active = execute(command)

            except sr.WaitTimeoutError:
                print("Timed out waiting for command. Going back to standby.")
                speak("Going to standby.")
                is_active = False

            except sr.UnknownValueError:
                pass

            except Exception as e:
                print("Error:", e)
