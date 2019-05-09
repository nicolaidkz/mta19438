import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import winsound
from scipy.fftpack import fft,fftfreq
from scipy.signal import fftconvolve
from scipy.signal import butter, lfilter
from scipy.io.wavfile import read
import pyaudio
import wave
import sys
import librosa, librosa.display
import IPython.display as ipd
import time

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print ("recording...")
frames = []

#winsound.Beep(1000,200) # Here we create a sound
#print ("Beep'd")

#time.sleep(3)

#winsound.Beep(1000,200) # Here we create a sound
#print ("Beep'd")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

audioFile = read("file.wav")
audioInputData = audioFile[1]
audioFileArray = np.array(audioFile[1])
#audioFileArray = np.hstack(audioFile[1])
print(audioFileArray)

x, sr = librosa.load('file.wav')
ipd.Audio(x, rate=sr)

r = np.correlate(x, x, mode='full')[len(x):]
print(x.shape, r.shape)



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

# Down here we calculate the distance, remember to substract the time delay
# between the played sound and mic


def distance_calc(time):
    speed = 343
    dist = time * speed
    return dist


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


print ("%.2f" % distance_calc(0.05) + " cm")

y = butter_bandpass_filter(audioFileArray, 1450, 1550, 44100, order=6)
plt.plot(y, label='bandpassed')
plt.ylabel('value')
plt.xlabel('sample')
plt.legend(loc='upper left')
plt.show()

plt.figure(figsize=(14, 5))
plt.plot(r)
plt.xlabel('Lag (samples)')
plt.show()

# plot the first 1024 samples
plt.plot(audioInputData)
# label the axes
plt.ylabel("Amplitude")
plt.xlabel("Time")
# set the title
plt.title("Sample Wav")
# display the plot
plt.show()