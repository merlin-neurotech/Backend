import ble2lsl
from ble2lsl.devices import muse2016 # Why do I have to import this seperately? This is dumb
import pylsl
import time
import numpy as np
import time
from functions import plotTimeDomain
from StreamStaff import getStream_info
from threads import runFunc
import threading


dummy_streamer = ble2lsl.Dummy(muse2016)
print("Here")
stream_info = pylsl.resolve_byprop("type", "EEG") #getStream_info(dummy_streamer)
print("Here")
stream = stream_info[0]
print("Here")
runFunc(functionToRun=plotTimeDomain, argsToRun={'stream_info':stream, 'channels':2, 'timewin':15})
print("done")
exit()




'''
for x in range(len(list1)):
    list1[x].insert(0) = list2[x]
'''
