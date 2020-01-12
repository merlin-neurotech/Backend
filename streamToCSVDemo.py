"""Demonstration of a function which takes a stream and writes it sample by sample to a CSV file"""

import ble2lsl
from ble2lsl.devices import muse2016
import pylsl
import csv
import os 

def csvWrite(streamObj, length, filename="merlin"):
    """Writes the samples of a stream to a CSV file
    Arguments:
        streamObj - a pylsl.StreamInlet object
        filename - the name you would like to give the file, excluding the .csv extension
        length - how many samples you would like to write. For example a length of 1 would yield 1 sample and 1 line
    """
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

#Below, the function is demonstrated by creating a dummy streamer and writing 1000 samples to a file
dummy_streamer = ble2lsl.Dummy(muse2016)

pylslResolvedStreams = pylsl.resolve_streams(wait_time=2.0)

streams = [[stream.source_id(), stream.type(), stream]
               for stream in pylslResolvedStreams]

for streamInfo in streams:
    if streamInfo[1] == 'EEG':
        EEGStreamInfo = streamInfo[2] 
        break

streamIn = pylsl.StreamInlet(EEGStreamInfo, max_buflen = 360, max_chunklen=0, recover=True)
streamIn.pull_sample()
csvWrite(streamIn, 1000, "test")
