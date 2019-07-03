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

        self.channels = 1
        self.format = pyaudio.paInt16

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk)

        self.stream.stop_stream()

    def record(self):
        print('Exceeded threshold, recording...')
        record = []
        curr = time.time()
        end = curr + self.dt

        while (curr < end and self.flag):
            audio_data = self.stream.read(self.chunk)
            audio_rms = rms(audio_data, 2)
            audio_db = 20*np.log10(audio_rms)
            #print(audio_db)
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

        self.flag = True
        if not self.threshold:
            self.setThreshold()

        print('Listening...')
        self.stream.start_stream()

        while self.flag:    
            audio_data = self.stream.read(self.chunk) #read size of buffer
            audio_rms = rms(audio_data, 2) #calculate rms_value 2 because data is organized in 16 bits
            audio_db = 20*np.log10(audio_rms)
            #print(audio_db) 
            if audio_db > self.threshold:
                self.record()
                print('Listening...')
        
        self.stream.stop_stream()
        print('Stopped.')

    def stop(self):
        self.flag = False

    def setThreshold(self):

        print('Setting threshold, listening {}s...').format(self.timetoset)
        self.stream.start_stream()

        record = ''
        curr = time.time()
        end = curr + self.timetoset
        while(curr < end):
            record += self.stream.read(self.chunk)
            curr = time.time()

        audio_rms = rms(record, 2)
        audio_db = 20*np.log10(audio_rms)
        self.threshold = audio_db + 5

        self.stream.stop_stream()
        print('Threshold set to {}dB.').format(self.threshold)
        

class ThreadAudioRecording(Thread):

    def __init__(self, object, func):
        Thread.__init__(self)
        self.object = object
        self.func = func

    def run(self):

        if self.func == 'listen':
            self.object.listen()
        elif self.func == 'stop':
            self.object.stop()
        elif self.func == 'set':
            self.object.setThreshold()

def runModule():
    str = ''
    audio = AudioRecording()
    
    th_set = ThreadAudioRecording(audio, 'set')
    th_set.start()
    th_set.join()
   
    while(str != 'start'):
        str = raw_input()

    while(str != 'stop'):
        th_exec = ThreadAudioRecording(audio, 'listen')
        th_stop = ThreadAudioRecording(audio, 'stop')
        th_exec.start()

        while(str != 'stop' and str != 'pause'):
            str = raw_input()

        th_stop.start()
        th_exec.join()
        th_stop.join()
               
        if(str == 'pause'):
            while(str != 'start' and str != 'stop'):
                str = raw_input()

if __name__ == "__main__":

    runModule()
