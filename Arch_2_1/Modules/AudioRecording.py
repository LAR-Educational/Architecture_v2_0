import pyaudio
import numpy as np
import wave
import time
import os
from audioop import rms
from threading import Thread

class AudioRecording:

    def __init__(self,
                RATE=44100, 
                THRESHOLD=None,
                CHUNK=1024,
                DT=3,
                TIMETOSET = 5,
                FOLDERNAME = 'audios'):

        self.rate = RATE
        self.threshold = THRESHOLD
        self.chunk = CHUNK
        self.dt = DT
        self.timetoset = TIMETOSET 
        self.foldername = FOLDERNAME

        self.flag = True
        self.channels = 1
        self.format = pyaudio.paInt16

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk)

    def record(self):
        print('Exceeded threshold, recording...')
        record = []
        curr = time.time()
        end = curr + self.dt

        while (curr < end and self.flag):
            audio_data = self.stream.read(self.chunk)
            audio_rms = rms(audio_data, 2)
            audio_db = 20*np.log10(audio_rms)
            print(audio_db)
            if audio_db > self.threshold:
                end = curr + self.dt
            curr = time.time()
            record.append(audio_data)

        print('{}s of threshold not exceeded, recording completed.').format(self.dt)
        self.write(b''.join(record))

    def write(self, audio_pack):

        curr_path = os.getcwd()
        dest_path = os.path.join(curr_path, self.foldername)

        if not os.path.isdir(dest_path): 
            os.mkdir(self.foldername)

        name = time.strftime("%m-%d-%Y-%H:%M:%S", time.localtime(time.time()))
        filename = os.path.join(dest_path, '{}.wav').format(name)

        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(audio_pack)
        wf.close()

        print('Audio saved.')

    def listen(self):

        if not self.threshold:
            print('Setting threshold, listening {}s...,').format(self.timetoset)
            self.setThreshold()
        print('Threshold set to {}dB').format(self.threshold)
        print('Listening...')

        while self.flag:    
            audio_data = self.stream.read(self.chunk) #read size of buffer
            audio_rms = rms(audio_data, 2) #calculate rms_value 2 because data is organized in 16 bits
            audio_db = 20*np.log10(audio_rms)
            print(audio_db) 
            if audio_db > self.threshold:
                self.record()
                print('Listening...')

    def stop(self):
        self.flag = False

    def setThreshold(self):
        record = ''
        curr = time.time()
        end = curr + self.timetoset
        while(curr < end):
            record += self.stream.read(self.chunk)
            curr = time.time()

        audio_rms = rms(record, 2)
        audio_db = 20*np.log10(audio_rms)
        self.threshold = audio_db

class ThreadAudioRecording(Thread):

    def __init__(self, object, num):
        Thread.__init__(self)
        self.object = object
        self.num = num

    def run(self):

        if self.num == 1:
            self.object.listen()
        else:
            self.object.stop()


if __name__ == "__main__":
    str = 'rodando'

    audio = AudioRecording()
    p1 = ThreadAudioRecording(audio, 1)
    p2 = ThreadAudioRecording(audio, 2)
    p1.start()

    while(str != 's'):
	    str = raw_input()
    p2.start()






