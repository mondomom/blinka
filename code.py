"""
This test will initialize the display using displayio and draw a solid green
background, a .bmp will be loaded in the middle, and some text that changes color.
"""
import board
import displayio
import terminalio
import time
from adafruit_display_text import label
from adafruit_st7789 import ST7789

spi = board.SPI()
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000) # Configure SPI for 24MHz
spi.unlock()
tft_cs = board.D5
tft_dc = board.D6

displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)

display = ST7789(display_bus, width=320, height=240, rotation=90)

# Make the display context
with open("/blinka.bmp", "rb") as bitmap_file:

    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x00FF00 # Bright Green
    # Create a Group to hold the TileGrid
    group = displayio.Group()

    bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
    group.append(bg_sprite)

    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter(), x=20, y=20)


    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Draw a label
    text_group = displayio.Group(max_size=5, scale=2, x=80, y=200)
    text = "Hello Blinka!"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFF0000)
    text_group.append(text_area) # Subgroup for text scaling
    group.append(text_group)


    # Add the Group to the Display
    display.show(group)




    # Loop forever so you can enjoy your image
    while True:
        time.sleep(1)
        text_area.color=0xFF00FF
        bg_sprite.pixel_shader[0] = 0xFF00FF
        time.sleep(1)
        text_area.color=0x00FF00
        bg_sprite.pixel_shader[0] = 0x00FF00
        time.sleep(1)
        pass