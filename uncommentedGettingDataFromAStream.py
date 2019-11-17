import ble2lsl
from ble2lsl.devices import muse2016
import pylsl

dummy_streamer = ble2lsl.Dummy(muse2016) 
print("Dummy streamer: " + str(dummy_streamer))  

pylslResolvedStreams = pylsl.resolve_streams(wait_time=2.0)


streams = [[stream.source_id(), stream.type(), stream]
               for stream in pylslResolvedStreams]


for streamInfo in streams:
    print(streamInfo)

for streamInfo in streams:
    if streamInfo[1] == 'EEG':
        EEGStreamInfo = streamInfo[2] 
        break

print(EEGStreamInfo)

streamIn = pylsl.StreamInlet(EEGStreamInfo,max_buflen = 360, max_chunklen=0,recover=True)
print(streamIn)

streamIn.open_stream() 

print(streamIn.pull_sample()) 

print(streamIn.pull_chunk()) 

#streamIn.__del__()
#EEGStreamInfo.__del__()
