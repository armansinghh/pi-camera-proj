"""
buttons (all wired to gnd, so we use the pi's internal pull-ups):
  shutter (gpio22)   press    -> take a photo, show it on the e-paper
  play/pause (gpio23) press   -> play / pause music
                      hold    -> toggle audio-only mode (shutter disabled)
  next (gpio26)       press   -> next song
                      hold    -> volume up
  prev (gpio27)       press   -> previous song
                      hold    -> volume down

NOTE: not tested on real hardware yet
"""
import threading
import time

from gpiozero import Button
from PIL import Image

import audio
import camera
import display

SHUTTER_PIN, PLAY_PIN, NEXT_PIN, PREV_PIN = 22, 23, 26, 27
VOLUME_HOLD = 0.6
MODE_HOLD = 1.5

player = None
audio_only = False
busy = threading.Lock()
pending = None


def show_pending():
    global pending
    if pending and display.ready():
        display.show(Image.open(pending))
        pending = None


def on_shutter():
    global pending
    if audio_only:
        print("audio only mode, camera is off")
        return
    if not busy.acquire(blocking=False):
        print("still busy with the last photo")
        return
    try:
        pending = camera.take_photo() 
        print("saved", pending)
        show_pending()
    finally:
        busy.release()


Button.was_held = False


def held(btn, action):
    btn.was_held = True
    action()


def released(btn, action):
    if not btn.was_held:
        action()
    btn.was_held = False


def toggle_audio_only():
    global audio_only
    audio_only = not audio_only
    print("audio only mode:", audio_only)


def setup():
    global player
    player = audio.Player()

    shutter = Button(SHUTTER_PIN)
    shutter.when_pressed = lambda: threading.Thread(target=on_shutter).start()

    play = Button(PLAY_PIN, hold_time=MODE_HOLD)
    play.when_released = lambda: released(play, player.toggle)
    play.when_held = lambda: held(play, toggle_audio_only)

    nxt = Button(NEXT_PIN, hold_time=VOLUME_HOLD, hold_repeat=True)
    nxt.when_released = lambda: released(nxt, player.next)
    nxt.when_held = lambda: held(nxt, player.volume_up)

    prev = Button(PREV_PIN, hold_time=VOLUME_HOLD, hold_repeat=True)
    prev.when_released = lambda: released(prev, player.prev)
    prev.when_held = lambda: held(prev, player.volume_down)

    return {"shutter": shutter, "play": play, "next": nxt, "prev": prev}


def tick():
    player.update()
    if pending and busy.acquire(blocking=False):
        try:
            show_pending()
        finally:
            busy.release()


def main():
    buttons = setup()
    print("ready")
    try:
        while True:
            tick()
            time.sleep(0.5)
    except KeyboardInterrupt:
        player.stop()


if __name__ == "__main__":
    main()