import serial
import speech_recognition as sr
import numpy as np
import time

# ==========================================
# SERIAL COMMAND KEYS SENT TO THE ARDUINO
# ==========================================
#
# A = Turn Living Room Light ON
# a = Turn Living Room Light OFF
#
# B = Turn Fan ON
# b = Turn Fan OFF
#
# C = Open Door
# c = Close Door
#
# D = Security System ON
# d = Security System OFF
#
# ==========================================

# -------------------------------
# CONFIGURATION
# -------------------------------

# Windows: "COM3"
# macOS: "/dev/tty.usbmodem1101" (change after connecting Arduino)
SERIAL_PORT = "COM3"

BAUD_RATE = 9600
NOISE_THRESHOLD = 500

# -------------------------------
# SERIAL CONNECTION
# -------------------------------

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# IMPORTANT FIX: Arduino reset delay
time.sleep(2)
arduino.reset_input_buffer()

print(f"[INFO] Connected to Arduino on {SERIAL_PORT}")

recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("[INFO] Calibrating microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("[INFO] Ready! Speak a command.\n")


# -------------------------------
# FUNCTIONS
# -------------------------------

def get_rms_volume(audio_data):
    samples = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
    rms = np.sqrt(np.mean(samples.astype(np.float64) ** 2))
    return rms


def send_signal(command):
    arduino.write((command + "\n").encode())
    arduino.flush()
    print(f"[SENT] {command}")


def process_voice(recognized_text):

    lowered = recognized_text.lower()

    print(f"[HEARD] {lowered}")

    # Light
    if "turn on light" in lowered or "light on" in lowered:
        send_signal("A")

    elif "turn off light" in lowered or "light off" in lowered:
        send_signal("a")

    # Fan
    elif "turn on fan" in lowered or "fan on" in lowered:
        send_signal("B")

    elif "turn off fan" in lowered or "fan off" in lowered:
        send_signal("b")

    # Door
    elif "open door" in lowered:
        send_signal("C")

    elif "close door" in lowered:
        send_signal("c")

    # Security
    elif "security on" in lowered:
        send_signal("D")

    elif "security off" in lowered:
        send_signal("d")

    else:
        print("[INFO] Command not recognised.")


# -------------------------------
# MAIN LOOP
# -------------------------------

print("Listening...")

try:

    while True:

        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

        volume = get_rms_volume(audio)

        print(f"Volume = {volume:.1f}")

        if volume < NOISE_THRESHOLD:
            print("Too quiet.")
            continue

        try:

            text = recognizer.recognize_google(audio)

            process_voice(text)

        except sr.UnknownValueError:
            print("Could not understand.")

        except sr.RequestError as e:
            print(e)

except KeyboardInterrupt:

    arduino.close()

    print("Program stopped.")

    # ==========================================
    #Declaration: The overall project design, logic, and implementation were developed by me. As this was my first time working with Arduino and Python integration, I used AI to assist with understanding concepts, improving code structure, adding comments, and debugging.
    #==========================================
