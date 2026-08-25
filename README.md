# pi-camera-proj
A camera that only remembers one photo (on screen, at least).

## What it is (more like "what it will be")
No gallery, no scrolling, the e-paper only ever shows your most recent shot. Every photo we take gets saved to storage too (and backs up to your laptop/phone when connected), so nothing's lost and the display just stays showing the last pic we took.

Made it from scratch: camera, e-paper driver, dithering, and (because why not) an mp3 player crammed into the same box. 

## Electronics

| Part |
|---|
| Waveshare 4inch e-Paper HAT+ (Spectra 6, color) |
| Raspberry Pi Zero 2 W |
| Raspberry Pi Camera Module 3 |
| PiSugar 3 |
| PCM5102A I2S DAC |
| MicroSD card |
| Buttons x4 |
| M3 screws |

## Wiring

![Wiring Schematic](./assets/wiring.png)

## Enclosure

![Enclosure Model](./assets/enclosure.png)

## Status
schematic done, enclosure in progress, nothing built yet

## Credits
Not a clone of [reFrame](https://github.com/kaloyaan/reframe), though that's what got me thinking about this