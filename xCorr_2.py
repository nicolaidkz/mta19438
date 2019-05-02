import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import winsound
from scipy.fftpack import fft,fftfreq
from scipy.signal import fftconvolve

winsound.Beep(3000,200) # Here we create a sound

# Down here we have the cross correlation and prints the correlated array

data1 = np.array([0,1,9,5])
data2 = np.array([0,1])
print (np.correlate(data1,data2,"full"))

# Here I have the function that does cross correlation and returns
# max val and at what position (time realated) is located in array
# with that position we can figure the distance

def similarity(template, test):
    corr = np.correlate(template, test, mode='same')
    for i in corr:
        max_val = max(corr)
        max_pos = corr.argmax()
        return max_val, max_pos
        
print (similarity(data1, data2))

#Down here we calculate the distance, remember to substract the time delay 
#between the played sound and mic

def distance_calc(time):
    speed = 343
    dist = time * speed
    return dist

print ("%.2f" % distance_calc(0.05) + " cm")