import pyaudio
import numpy as np
import sys
import matplotlib.pyplot as plt

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100 #hz
delay = np.int(np.round(0.05*RATE))
filterCoef = 0.5

p = pyaudio.PyAudio()

streamIn = p.open(format=p.get_format_from_width(WIDTH),
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)


def combfiltering(inputSignal, filterCoef, delay, feedBackIsUsed=False):
    nData = np.size(inputSignal)
    outputSignal = np.zeros(nData)
    for n in np.arange(nData):
        if n < delay:
            outputSignal[n] = inputSignal[n]
        else:
            if feedBackIsUsed:
                outputSignal[n] = inputSignal[n]+filterCoef*outputSignal[n-delay]
            else:
                print("hello")
                outputSignal[n] = inputSignal[n]+filterCoef*inputSignal[n-delay]
    return outputSignal


if __name__ == "__main__":
    print("* recording")
    for i in range(0, int(RATE / CHUNK * sys.maxsize)):
        data = np.fromstring(streamIn.read(CHUNK), dtype=float)
        modifiedSignal = combfiltering(data, filterCoef, delay, False)
        streamIn.write(modifiedSignal, CHUNK)

    print("*Stopped Recording")

    streamIn.stop_stream()
    streamIn.close()
    p.terminate()
