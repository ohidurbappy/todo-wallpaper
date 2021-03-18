import os
import ctypes
from PIL import Image, ImageDraw, ImageFont
import time


APP_PATH=os.path.abspath(os.path.dirname(__file__))
FONT_FILENAME="OpenSans-Regular.ttf"
BACKGROUND_FILENAME="1.png"
TODO_FILENAME="todo.txt"
OUTPUT_DIR=os.path.join(APP_PATH,'output')
OUTPUT_IMAGE_PATH=os.path.join(APP_PATH,'output','background.png')


def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path , 3)

def strikethrough(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

todos=[line.strip() for line in open(os.path.join(APP_PATH,TODO_FILENAME),encoding='utf-8')]

image=Image.open(os.path.join(APP_PATH,"background",BACKGROUND_FILENAME))
fnt=ImageFont.truetype(os.path.join(APP_PATH,'fonts',FONT_FILENAME),32)

d1=ImageDraw.Draw(image)

width,height=image.size

w=width-round(width/4)
h=round(height/5)

for todo_item in todos:
    d1.text((w, h), todo_item, font=fnt, fill =(255, 255, 255))
    h+=34


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

image.save(OUTPUT_IMAGE_PATH)
time.sleep(1)
set_wallpaper(OUTPUT_IMAGE_PATH)

