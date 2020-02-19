import ble2lsl
from ble2lsl.devices import muse2016 # Why do I have to import this seperately? This is dumb
import pylsl
import time
import numpy as np
import time
from functions import plotTimeDomain, fft, plotFreqDomain
from StreamStaff import getStream_info
from threads import runFunc
import threading
import queue


dummy_streamer = ble2lsl.Dummy(muse2016)
stream_info = pylsl.resolve_byprop("type", "EEG") #getStream_info(dummy_streamer)
stream = stream_info[0]
#psd = fft(stream, output_stream_name='psd')

#runFunc(functionToRun=plotFreqDomain, argsToRun={'stream_info':psd, 'chunkwidth':129})
#runFunc(functionToRun=plotTimeDomain, argsToRun={'stream_info':stream, 'channels':2, 'timewin':15})
runFunc(functionToRun=fft, argsToRun={'input_stream':stream, 'output_stream_name':'lalala'})
#runFunc(functionToRun=fft, argsToRun={'input_stream':stream, 'output_stream_name':'test2'})

psd = pylsl.resolve_byprop('type', 'PSD')
psd = psd[0]
plotFreqDomain(psd,chunkwidth=129)




'''
for x in range(len(list1)):
    list1[x].insert(0) = list2[x]
'''
