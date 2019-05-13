import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io.wavfile import read
import pyaudio
import librosa, librosa.display
import wave
import IPython.display as ipd

#-------THIS IS ALL THE INITIAL STUFF WE NEED------
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 22050
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav" #------WE SAVE THE AUDIO INPUT TO A WAV FILE WE USE LATER----

audio = pyaudio.PyAudio()



#------THIS IS WHERE WE OPEN THE MICROPHONE INPUT AND START RECORDING------
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("recording...")
frames = []

#------THIS FORLOOP RUNS UNTIL THERE HAS PASSED 5 SECOUNDS-----
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")


#----- THIS SHUTS DOWN THE MICROFONE AND AND STOPS RECORDING----#
stream.stop_stream()
stream.close()
audio.terminate()


#------THIS IS THE PLACE WHERE WE LOAD IN THE SOUND FILE---
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()


#----- THIS IS WHERE WE LOAD THE SOUND FILE INTO AN ARRAY---
audioFile = read("file.wav")
#audioInputData = audioFile[1] #WHAT IS THIS USED FOR???
#audioFileArray = np.array(audioFile)
audioFileArray = np.hstack(audioFile[1])
#print(audioFileArray)

print(audioFileArray)

def butter_bandpass(lowcut, highcut, fs, order = 6):
    nyq = 1 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order = 6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


y_cre = butter_bandpass_filter(audioFileArray, 1600, 1900, 22050, order = 6) # THIS Y NEEDS TO RUN TROUGH THE CORRELATION!!!!!!!

print(y_cre)

r = np.correlate(y_cre, y_cre, mode='full')

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



#One_D_array = np.reshape(y_cre,(-1,2))
#print(One_D_array)



#print(r)
# label the axes
# display the plot
# set the title
# plot the first 1024 samples

#NOTES

# winsound.Beep(1000,200) # Here we create a sound
# print ("Beep'd")
# time.sleep(3)
# winsound.Beep(1000,200) # Here we create a sound
# print ("Beep'd")



#def distance_calc(time):
    #speed = 343
    #dist = time * speed
    #return dist