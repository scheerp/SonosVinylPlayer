import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 2)
pixels[0] = (40, 0, 80)
pixels[1] = (0, 50, 10)

