import serial
import speech_recognition as sr
import numpy as np

# ==========================================
# SERIAL COMMAND KEYS SENT TO THE ARDUINO
# ==========================================
#
# A = Turn Living Room Light ON
# a = Turn Living Room Light OFF
#
# K = Turn Kitchen Light ON
# k = Turn Kitchen Light OFF
#
# B = Open Door
# b = Close Door
#
# G = Good Boy (Servo Wag)
#
# P = Party Mode
#
# ==========================================

# -------------------------------
# CONFIGURATION
# -------------------------------

# Windows: "COM3"
SERIAL_PORT = "/dev/cu.usbmodem112401"
BAUD_RATE = 9600
NOISE_THRESHOLD = 500

# -------------------------------
# SERIAL CONNECTION
# -------------------------------

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
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
    arduino.write(command.encode())
    print(f"[SENT] {command}")


def process_voice(recognized_text):

    lowered = recognized_text.lower()

    print(f"[HEARD] {lowered}")

    # All Lights
    if "all lights on" in lowered or "turn on all lights" in lowered:
        send_signal("L")

    elif "all lights off" in lowered or "turn off all lights" in lowered:
        send_signal("l")

    # Living Room Light
    elif "turn on living room light" in lowered or "living room light on" in lowered:
        send_signal("A")

    elif "turn off living room light" in lowered or "living room light off" in lowered:
        send_signal("a")

    # Kitchen Light
    elif "turn on kitchen light" in lowered or "kitchen light on" in lowered:
        send_signal("K")

    elif "turn off kitchen light" in lowered or "kitchen light off" in lowered:
        send_signal("k")

    # Door
    elif "open door" in lowered:
        send_signal("B")

    elif "close door" in lowered:
        send_signal("b")

    # Fun Mode
    elif "good boy" in lowered:
        send_signal("G")

    elif "party mode" in lowered:
        send_signal("P")

    else:
        print("[INFO] Command not recognised.")


# -------------------------------
# MAIN LOOP
# -------------------------------

print("Listening...")

try:

    while True:

        with microphone as source:
            audio = recognizer.listen(source, phrase_time_limit=3)

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
    # Declaration: The overall project design, logic, and implementation were developed by me. As this was my first time working with Arduino and Python integration, I used AI to assist with understanding concepts, improving code structure, adding comments, and debugging.
    # ==========================================
