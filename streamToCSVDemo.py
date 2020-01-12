import ble2lsl
from ble2lsl.devices import muse2016
import pylsl
import csv
import os 

def csvWrite(streamObj, filename, length):
    if not isinstance(streamObj, pylsl.StreamInlet):
        raise Exception("Argument streamObj must be a pylsl.StreamInlet object")
    
    try:
        filen = str(filename) + ".csv"
    except:
        raise Exception("Input filename could not be cast to string")
    
    if length <= 0:
        raise Exception("File length cannot be less than or equal to zero")
    
    with open(os.getcwd() + "\\" + filen, 'w', newline="") as csvFile:
        csvWriter = csv.writer(csvFile)
        for i in range(0, length-1):
            streamData = streamObj.pull_sample()
            csvWriter.writerow(streamData[0])

    csvFile.close()

dummy_streamer = ble2lsl.Dummy(muse2016)

pylslResolvedStreams = pylsl.resolve_streams(wait_time=2.0)

streams = [[stream.source_id(), stream.type(), stream]
               for stream in pylslResolvedStreams]

for streamInfo in streams:
    if streamInfo[1] == 'EEG':
        EEGStreamInfo = streamInfo[2] 
        break

streamIn = pylsl.StreamInlet(EEGStreamInfo,max_buflen = 360, max_chunklen=0,recover=True)
streamIn.pull_sample()
csvWrite(streamIn, "test", 1000)
