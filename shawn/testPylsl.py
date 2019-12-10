import ble2lsl
from ble2lsl.devices import muse2016 # Why do I have to import this seperately? This is dumb
import pylsl
import time
import numpy as np
import time
from functions import plotTimeDomain, plotFreqDomain

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

print("have the steam info object")

# Create stream inlet to accept stream object data
plotFreqDomain(stream, 12, title='EEG Data')

print("past")
#print('\nChannels: %d' % stream.channel_count())
#print('Time: %f', time.time())

#print('\nEEG Sample: ')
# Sometimes pull_sample times out, also sometimes it returns different sized arrays for the samples. Not consistently getting a sample for all channels
# while(1):
#     x = streamIn.pull_chunk()
#     if all(x):
#         print(x)
#     #if not np.shape(x) == (2, 0):
#         print(np.shape(x))
#         #print(time.time())
#         #print(time.time() + streamIn.time_correction())

# Delete objects and stop stream
#streamIn.__del__() # Throws weird errors
#EEGstream.__del__() # Also throws weird errors
dummy_streamer.stop()
