import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io.wavfile import read
import pyaudio
# import librosa, librosa.display
import wave
# import IPython.display as ipd
import winsound
np.set_printoptions(threshold=np.inf)

def peakDetect(l):  # b is true returns a list of correlation values at peaks, false returns a list of indexes
    idx = len(l)
    idx = idx // 2  #start halfway through list (skip negative times)
    # thresh = 0.05
    tempPeaks = [[], []]
    up = False
    while True:
        if l[idx] < l[(idx - 1)] and up is True:
            tempPeaks.append([idx, l[idx]]) # Adds index and corr of peak
            up = False
        elif l[idx] > l[idx - 1] and up is False:
            up = True
        idx += 1
        if idx >= len(l):
            break
    return tempPeaks

def corrDetector(arr, threshLow, threshHigh):  # Ignores first corr (at 0), gets next one above thresh, returns index
    tb = False
    ind = 3
    while tb is False:
        if arr[ind][1] < threshLow and arr[ind][1] > 0:
            tb = True
        ind += 1
        if ind >= len(arr):
            return -1
    while tb is True:
        if arr[ind][1] > threshHigh:
            return arr[ind][0]
        ind += 1
        if ind >= len(arr):
            return -2

def timeToDist(delay, rate, speed):  # Pass this delay before sound is heard, sampling rate of sound, and speed of sound
    sampToSec = 1 / rate
    tempTime = delay * sampToSec
    tempDist = tempTime * speed
    return tempDist


# pass the data array, start position, and a threshold. Returns first instance above thresh, or -1 if none
def findDelay(arr, start, thresh):
    ln = len(arr)
    while j + start < ln:
        if arr[start + j] > thresh:
            return (start + j)
        j = j + 1
    else:
        return -1


# -------THIS IS ALL THE INITIAL STUFF WE NEED------
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
CHUNK = 1024
RECORD_SECONDS = 1
FREQ = 1700
WAVE_OUTPUT_FILENAME = "file.wav"  # ------WE SAVE THE AUDIO INPUT TO A WAV FILE WE USE LATER----

audio = pyaudio.PyAudio()

# ------THIS IS WHERE WE OPEN THE MICROPHONE INPUT AND START RECORDING------
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("recording...")
frames = []
#winsound.Beep(FREQ, 100)

# ------THIS FORLOOP RUNS UNTIL THERE HAS PASSED 5 SECOUNDS-----
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    if i == 2 or i == 4:
        winsound.Beep(FREQ, 100)
print("finished recording")

# ----- THIS SHUTS DOWN THE MICROFONE AND AND STOPS RECORDING----#
stream.stop_stream()
stream.close()
audio.terminate()

# ------THIS IS THE PLACE WHERE WE LOAD IN THE SOUND FILE---
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

# ----- THIS IS WHERE WE LOAD THE SOUND FILE INTO AN ARRAY---
audioFile = read("file.wav")
# audioInputData = audioFile[1] #WHAT IS THIS USED FOR???
#audioFileArray = np.array(audioFile)
audioFileArray = np.hstack(audioFile[1])

print(audioFileArray)



def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 1 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


y_cre = butter_bandpass_filter(audioFileArray, FREQ-50, FREQ+50, 11025,
                               order=6)  # THIS Y NEEDS TO RUN TROUGH THE CORRELATION!!!!!!!

# print(y_cre)

r = np.correlate(y_cre, y_cre, mode='full')
r = r / r.max()

peaks = peakDetect(r)
# for i in peaks:
#     print(i)
delay = corrDetector(peaks, 0.08, 0.10)   # change 2nd and 3rd values to what works best
if delay == -1:
    print("Never went below threshLow")
if delay == -2:
    print("Never went above threshHigh")
else:
    delay = delay - (len(r)/2)
    print("delay: " + str(delay))
    dist = timeToDist(delay, RATE, 343)
    print("distance = " + str(dist) + " meters")




plt.plot(audioFileArray, label='raw data')
plt.ylabel('value')
plt.xlabel('sample')
plt.legend(loc='upper left')
plt.show()

plt.plot(y_cre, label='bandpassed')
plt.ylabel('value')
plt.xlabel('sample')
plt.legend(loc='upper left')
plt.show()

plt.plot(r, label='correlated')
plt.ylabel('value')
plt.xlabel('sample')
plt.legend(loc='upper left')
plt.show()

# One_D_array = np.reshape(y_cre,(-1,2))
# print(One_D_array)


# print(r)
# label the axes
# display the plot
# set the title
# plot the first 1024 samples

# NOTES

# winsound.Beep(1000,200) # Here we create a sound
# print ("Beep'd")
# time.sleep(3)
# winsound.Beep(1000,200) # Here we create a sound
# print ("Beep'd")


# def distance_calc(time):
# speed = 343
# dist = time * speed
# return dist
