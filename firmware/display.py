"""
shows an image on the spectra 6 e-paper (waveshare 4inch e-paper hat+ (E)).

needs waveshare's library: find the `waveshare_epd` folder inside their demo
(4inch_e-Paper_E.zip) and copy it into firmware/lib/

NOTE: not tested yet, no hardware. the method names follow waveshare's demo
(epd_4in0e_test.py) will check them against it when the display arrives.
"""
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from waveshare_epd import epd4in0e  # noqa: E402
from dither import prepare  # noqa: E402

MIN_GAP = 180  # seconds. waveshare recommends at least 3 min between refreshes
STAMP = os.path.join(os.path.dirname(__file__), ".last_refresh")


def _seconds_since_last_refresh():
    try:
        with open(STAMP) as f:
            return time.time() - float(f.read())
    except (OSError, ValueError):
        return MIN_GAP


def ready():
    # true if enough time has passed since the last refresh
    return _seconds_since_last_refresh() >= MIN_GAP


def show(img, force=False):
    # dither + display a PIL image. returns False if it's too soon since the last refresh
    if not force and not ready():
        return False

    img = prepare(img)
    epd = epd4in0e.EPD()
    try:
        epd.init()
        epd.display(epd.getbuffer(img))  # takes ~19s
        with open(STAMP, "w") as f:
            f.write(str(time.time()))
    finally:
        epd.sleep()  # always sleep after a refresh
    return True