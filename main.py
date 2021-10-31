import os
import ctypes
from PIL import Image, ImageDraw, ImageFont,ImageOps
import time
import sys


def set_wallpaper(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path , 3)

def strikethrough(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def get_dominant_color(pil_img):
    img = pil_img.copy()
    #img=ImageOps.invert(img)
    img.convert("RGB")
    img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color


def get_screen_size():
    cmd = "wmic path Win32_VideoController get CurrentVerticalResolution,CurrentHorizontalResolution"
    (x,y) = tuple(map(int,os.popen(cmd).read().split()[-2::]))
    return (x,y)


APP_PATH=os.path.abspath(os.path.dirname(__file__))
TODO_FILENAME="todo.txt"
OUTPUT_DIR=os.path.join(APP_PATH,'output')
OUTPUT_IMAGE_PATH=os.path.join(APP_PATH,'output','background.png')

# default configurations
c_font_name="OpenSans-Regular.ttf"
c_font_name="lucida-console.ttf"
c_background="img19.jpg"
c_title="Todo"
c_font_size=22

thismodule = sys.modules[__name__]

def process_instruction(instruction:str):
    instruction=instruction.strip("[")  
    instruction=instruction.strip("]")
    try:  
        var,val=instruction.split("=")
        c_var="c_"+var
        if c_var in globals():
            # setattr(thismodule,"c_"+var,val)
            if val.isnumeric():
                val=int(val)
            globals()[c_var]=val

    except ValueError:
        pass
    
    
        
    


lines=[line for line in open(os.path.join(APP_PATH,TODO_FILENAME),encoding='utf-8')]

todos=[]

# read the configuration
for line in lines:
    pre_line=line.strip()
    if pre_line.startswith("[") and pre_line.endswith("]"):
        process_instruction(pre_line)
    else:
        todos.append(line)




image=Image.open(os.path.join(APP_PATH,"background",c_background))

basewidth = get_screen_size()[0]
wpercent = (basewidth/float(image.size[0]))
hsize = int((float(image.size[1])*float(wpercent)))
image = image.resize((basewidth,hsize), Image.ANTIALIAS)



fnt=ImageFont.truetype(os.path.join(APP_PATH,'fonts',c_font_name),c_font_size)
d1=ImageDraw.Draw(image)

width,height=image.size

x=width-round(width/4)*1
y=round(height/5)

w, h = fnt.getsize(c_title)
w+=10
h+=2

lCenter=(((width-x)-w/2)/6)*1


# (2,108,248)
d1.rectangle((x+lCenter, y, x + w+lCenter, y + h), fill=get_dominant_color(image))



d1.text((x+5+lCenter, y), c_title, font=fnt, fill =(255, 255, 255,255))
y+=c_font_size+2

for todo_item in todos:
    d1.text((x, y), todo_item, font=fnt, fill =(255, 255, 255))
    y+=c_font_size+2


if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

image.save(OUTPUT_IMAGE_PATH)
time.sleep(1)
set_wallpaper(OUTPUT_IMAGE_PATH)

