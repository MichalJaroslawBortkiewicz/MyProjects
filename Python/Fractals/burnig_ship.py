from PIL import Image, ImageDraw
from math import fabs

image_width = 1200
image_height = 1200
recursion = 255
scale = 4800

display = Image.new('RGB',(image_width,image_height),(0,0,0))
draw = ImageDraw.Draw(display)

Color_pallete = []

def Create_Color_Set():
    initial_color = [[0, 255, 255], [0, 0, 255], [255, 0, 255],[255, 0, 0],[255, 255, 0],[0, 255, 0]]
    final_color   = [[0, 0, 255], [255, 0, 255], [255, 0, 0],[255, 255, 0],[0, 255, 0],[0, 255, 255]]
    global Color_pallete
    Color_pallete = [initial_color[0]]
    for i in range (len(initial_color)):
        color_change = [0,0,0]
        for j in range (3):
            if initial_color[i][j] < final_color[i][j]:
                color_change[j] = 1
            elif initial_color[i][j] == final_color[i][j]:
                color_change[j] = 0
            elif initial_color[i][j] > final_color[i][j]:
                color_change[j] = -1
        for j in range(255):
            Old_color = Color_pallete[len(Color_pallete)-1]
            New_color = [Old_color[0]+color_change[0],Old_color[1]+color_change[1],Old_color[2]+color_change[2]]
            Color_pallete.append(New_color)

def In_Set(c):
    n = 0
    z = 0
    while abs(z) <= 2 and n < recursion:
        z = pow(complex(abs(z.real),abs(z.imag)),2)+c
        n += 1
    return n

def Mandelbrot():
    for x in range(0,image_width+1):
        for y in range(0,image_height+1):
            n = In_Set(complex(x/scale-1.875,y/scale-0.1875))
            if n == recursion:
                color = (0,0,0)
            else:
                color = (tuple(Color_pallete[int(len(Color_pallete)*n/255)]))
            draw.point([x,y],color)

Create_Color_Set()
Mandelbrot()
display.save('Burning Ship.png', 'PNG')