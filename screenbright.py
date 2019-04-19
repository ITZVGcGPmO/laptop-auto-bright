import cv2
import numpy
import time
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
cap = cv2.VideoCapture(0)  #ignore the errors
cap.set(3, 640) #width
cap.set(4, 480) #height
# this is a plot to map camera brightness to backlight brightness. 
# you can visualize it with a tool like https://plot.ly/create/line-graph or https://www.rapidtables.com/tools/line-graph.html
brightvl = [[0.0, 18],
            [0.1, 18],
            [0.13, 110],
            [0.43, 110],
            [0.46, 386],
            [0.49, 400],
            [0.52, 921],
            [1.0, 921]]
# this function calculates the backlight(y) value of a given camera(x) value.
def backlight_level(cam):
    for secnum, high in enumerate(brightvl):
        if high[0] > cam:
            low = brightvl[secnum-1]
            xoff = high[0]-low[0]
            yoff = high[1]-low[1]
            camoff = cam-low[0]
            return(int(low[1]+(yoff*camoff/xoff)))
avg = []
lastbr = 99
brightness = 5
while True:
    app = cap.read()[-1].mean(axis=0).mean(axis=0).mean(axis=0)/255
    avg.append(app)
    print(app)
    if len(avg) > 4:
        avg.pop(0)
        average = sum(avg)/len(avg)
        # if light is "stable"
        # and brightness is different from last brightness(no backlight flickers)
        if average+0.01>avg[-1]>average-0.01 and (brightness>avg[-1]+0.015 or brightness<avg[-1]-0.015):
            brightness = average
            print(f'set brightness! {brightness}, {backlight_level(brightness)}')

            open('/sys/class/backlight/intel_backlight/brightness', 'w').write(str(backlight_level(brightness)))
    time.sleep(1)
