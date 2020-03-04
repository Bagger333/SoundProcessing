import pyaudio
import numpy as np
import sys


CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 48000 #hz

p = pyaudio.PyAudio()

streamIn = p.open(format=p.get_format_from_width(WIDTH),
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  output=True,
                  frames_per_buffer=CHUNK)


if __name__ == "__main__":
    print("* recording")
    for i in range(0, int(RATE / CHUNK * sys.maxsize)):
        data = np.fromstring(streamIn.read(CHUNK), dtype=np.int16)
        streamIn.write(data, CHUNK)
        print(data)

    print("*Stopped Recording")

    streamIn.stop_stream()
    streamIn.close()
    p.terminate()
