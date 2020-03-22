import pyaudio
import numpy as np
import sys
import matplotlib.pyplot as plt

CHUNK = 30 #number / 2 = Samples gotten
WIDTH = 2
CHANNELS = 2
RATE = 44100 #hz
modulationDigFreq = 2*np.pi*20/RATE # rad/sample
modulationAmp = 0.4
filterCoef = 0.5
delay = np.int(np.round(0.15*RATE)) # samples

p = pyaudio.PyAudio()

streamIn = p.open(format=p.get_format_from_width(WIDTH),
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)

def addTremelo(inputSignal, modulationAmp, modulationDigFreq):
    nData = np.size(inputSignal)
    samplingIndices = np.arange(nData)
    modulatingSignal = 1-modulationAmp*np.cos(modulationDigFreq*samplingIndices)
    return inputSignal

def combfiltering(inputSignal, filterCoef, delay, feedBackIsUsed):
    nData = np.size(inputSignal)
    outputSignal = np.zeros(nData)
    for n in np.arange(nData):
        if n < delay:
            outputSignal[n] = inputSignal[n]
        else:
            if feedBackIsUsed:
                print("hello")
                outputSignal[n] = inputSignal[n]+filterCoef*outputSignal[n-delay]
            else:
                outputSignal[n] = inputSignal[n]+filterCoef*inputSignal[n-delay]
    return outputSignal


print("* recording")
while 1:
    dataN = streamIn.read(CHUNK)
    data = np.fromstring(dataN)
    #print(data)
    modifiedSignal = addTremelo(data,modulationAmp, modulationDigFreq)
    #modifiedSignal = combfiltering(data, filterCoef, delay, True)
    streamIn.write(data, CHUNK)

print("*Stopped Recording")

streamIn.stop_stream()
streamIn.close()
p.terminate()
