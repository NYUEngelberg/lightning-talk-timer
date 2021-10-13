# Circuit Playground NeoPixel
import time
import board
import neopixel
import digitalio

#stuff specific to the sound part
import array
import math

####Light'n button stuff ######

#set up the pixels
pixels = neopixel.NeoPixel(board.A2, 30, brightness=0.8, auto_write=False)

#sets the button variable
#button = digitalio.DigitalInOut(board.BUTTON_A)
#button = digitalio.DigitalInOut(board.A5)
button = digitalio.DigitalInOut(board.A5)

#makes pushing the button activate it
#button.switch_to_input(pull=digitalio.Pull.DOWN)
button.switch_to_input(pull=digitalio.Pull.UP)


led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

#color variables
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

color_chase_wait_time = 0.02

#####Audio stuff########

try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

FREQUENCY = 440  # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, recommended!

# Generate one period of sine wav.
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = AudioOut(board.SPEAKER)
sine_wave_sample = RawSample(sine_wave)

def yellow_flash(FLASH_TIME):
    pixels.fill(BLACK)
    pixels.show()
    time.sleep(FLASH_TIME)

    pixels.fill(YELLOW)
    pixels.show()
    time.sleep(FLASH_TIME)



#####rest of code######

def color_chase(color, wait):
    for i in range(30):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    #time.sleep(1)

while True:
    if button.value: #if button is pushed

        #green during the first ~40 seconds? (need to update time for all of this)
        pixels.fill(GREEN)
        pixels.show()
        led.value = True
        time.sleep(45)


        #yellow flashing for ~10 seconds?
        pixels.fill(YELLOW)
        pixels.show()
        time.sleep(2)

        yellow_flash(.5)
        yellow_flash(.5)
        yellow_flash(.5)
        yellow_flash(.5)
        yellow_flash(.5)
        yellow_flash(.5)
        yellow_flash(.5)
        yellow_flash(.5)



        #color chase for last ~5 seconds?
          # Increase the number to slow down the color chase
        color_chase(YELLOW, color_chase_wait_time)
        color_chase(CYAN, color_chase_wait_time)
        color_chase(BLUE, color_chase_wait_time)
        color_chase(PURPLE, color_chase_wait_time)
        color_chase(BLACK, color_chase_wait_time)
        color_chase(RED, color_chase_wait_time)

        #will beep for the numer of seconds in time.sleep()
        audio.play(sine_wave_sample, loop=True)
        time.sleep(2)
        audio.stop()

        #red time's up before next start
        pixels.fill(RED)
        pixels.show()
        time.sleep(3)

    else:
        pixels.fill(BLACK)
        pixels.show()
        led.value = False
    time.sleep(0.01)
