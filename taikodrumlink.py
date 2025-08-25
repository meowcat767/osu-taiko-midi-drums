import rtmidi
from evdev import UInput, ecodes as e
import time

# Map MIDI notes to key codes and names
MIDI_TO_KEY = {
    45: (e.KEY_D, "High Tom"),
    48: (e.KEY_F, "Low Tom"),
}

# Setup virtual keyboard
ui = UInput(events={e.EV_KEY: [key for key, _ in MIDI_TO_KEY.values()]}, name="MIDI Drum Keyboard")

# Setup MIDI input
midiin = rtmidi.MidiIn()
ports = midiin.get_ports()
print("Available MIDI ports:", ports)

# Open the Edrum port
midiin.open_port(1)
print(f"Opened MIDI port: {ports[1]}")

def note_on(note, velocity):
    entry = MIDI_TO_KEY.get(note)
    if entry:
        key, name = entry
        ui.write(e.EV_KEY, key, 1)  # Key press
        ui.write(e.EV_KEY, key, 0)  # Key release
        ui.syn()
        print(f"[{time.strftime('%H:%M:%S')}] {name} hit! Velocity: {velocity}")

print("Listening for High/Low Tom...")

while True:
    msg = midiin.get_message()
    if msg:
        message, delta_time = msg
        status, note, velocity = message
        if status == 153 and velocity > 0:  # Note On for your kit
            note_on(note, velocity)
