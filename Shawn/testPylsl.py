import ble2lsl
from ble2lsl.devices import muse2016 # Why do I have to import this seperately? This is dumb
import pylsl
import time
import numpy as np
import time
from functions import plotTimeDomain, plotFreqDomain, fft

########################
## Create a stream
########################
dummy_streamer = ble2lsl.Dummy(muse2016) #Using a dummy for now. We need some fuckin Muses. Why does most of the DEV TEAM not have any muses???


########################
## Find (Resolve) Stream
########################
streams = pylsl.resolve_byprop("type", "EEG", timeout=5) #type: EEG, minimum return streams = 1, timeout after 5 seconds
stream = streams[0]
#stream_info = getStream_info(dummy_streamer)
#sam trying his new code with your thing


fft(stream)
#plotTimeDomain(stream, 12, title='EEG Data')


dummy_streamer.stop()
