import ble2lsl as bl 
from ble2lsl.devices import muse2016, ganglion
from pylsl import StreamInlet, resolve_byprop, StreamOutlet #receiving the EEG signals 
import time
import numpy as np 
import bokeh
import pylsl as lsl

# this is the first revision of convert.py from Samuel White 
# taking alot of insporation from the BCI-Workshop code

class Convert:
    
    def __init__(self, device, max_chunklen = 0 ,stream_type = 'EEG'):
        
        streams = resolve_byprop('type', stream_type , timeout=2)
        if len(streams) == 0:
            raise RuntimeError('no EEG stream found')
        

        inlet, timecorrect,info,descrition,sampling_f,num_channels = self.get_Stream_Info(streams)
        
        ## getting the names of the channels, not sure if this is needed 
        ch = descrition.child('channels').first_child()
        self.ch_names = [ch.child_value('label')]
        for i in range(1, num_channels):
            ch = ch.next_sibling()
            self.ch_names.append(ch.child_value('label'))


        ## getting the buffer lengths, epoch lengths, overlap 
        buffer_len = 15 ## change to a user input (or from device)
        epoch_len = 1 #same as above comment 
        overlap_len = 0.8 # this is also dependent of the device file 

        
        

    def get_Stream_Info(self, streams):
        inlet = StreamInlet(streams[0], max_chunklen=12, recover=False) ## create a getter to change the chuncklength based on the device
        timecorrect = inlet.time_correction() # gets the time correction of the two buffers 
        info = inlet.info()
        descrition = info.desc()
        fs = int(info.nominal_srate())
        num_channels = info.channel_count()
        return inlet,timecorrect, info, descrition, fs, num_channels

    #def index_Channels(self):
        #index_channel = args.channels