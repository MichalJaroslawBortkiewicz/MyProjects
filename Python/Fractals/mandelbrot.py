from PIL import Image, ImageDraw

image_width = 1500
image_height = 1500
recursion = 255
scale = 600

display = Image.new('RGB',(image_width,image_height),(0,0,0))
draw = ImageDraw.Draw(display)

def In_Set(c):
    n = 0
    z = 0
    while abs(z) <= 2 and n < recursion:
        z = z*z+c
        n += 1
    return n

def Mandelbrot():
    for x in range(0,image_width+1):
        for y in range(0,image_height+1):
            n = In_Set(complex(x/scale - 2,y/scale-(5/4)))
            if n == recursion:
                color = (0,0,0)
            else:
                color = (255,int(255-255/n),0)
            draw.point([x,y],color)

Mandelbrot()
display.save('Mandelbrot.png', 'PNG')