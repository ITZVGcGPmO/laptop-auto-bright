import cv2
import numpy
import time
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

cap = cv2.VideoCapture(0)  #ignore the errors
cap.set(3, 640) #width
cap.set(4, 480) #height
cap.set(10, 0) #brightness
cap.set(11, 50) #contrast
cap.set(12, 64) #saturation
cap.set(13, 0) #hue

avg = []
lastbr = 99
brightness = 5
while True:
    lvl = clamp(((cap.read()[-1].mean(axis=0).mean(axis=0).mean(axis=0)/255)*4.5)-1.2,0,1)
    avg.append(lvl)
    if (len(avg) > 5):
        avg.pop(0)
        brightness = int(((sum(avg)/float(len(avg))*10)+brightness)/2)
        outbright = str(14+clamp(2**brightness,0,900))
        if (lastbr != brightness):
            open('/sys/class/backlight/intel_backlight/brightness', 'w').write(outbright)
            print('set brightness to '+str(brightness)+' ('+outbright+')')
        lastbr = brightness
        time.sleep(1.5)
    