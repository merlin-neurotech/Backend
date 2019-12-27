import ble2lsl
from ble2lsl.devices import muse2016
import pylsl

#Note that this is not at all what the final product will look like: it's just a simple script and a demonstration of how pylsl works

dummy_streamer = ble2lsl.Dummy(muse2016) #Using a dummy for now. We need some Muses
print("Dummy streamer: " + str(dummy_streamer))#Prints the address of the streamer to see if it was initialized correctly

pylslResolvedStreams = pylsl.resolve_streams(wait_time=2.0)
#wait time is how long pylsl spends searching for streams. Make it higher if your streamer isn't working.
#if you need to go higher than 5 then that means the problem is likely elsewhere
#note that resolve_byprop is preferred over resolve_streams

streams = [[stream.source_id(), stream.type(), stream]
               for stream in pylslResolvedStreams]
#Makes a list of lists. Each list has three elements: the ID of the device the stream is coming from,
#the type of stream, and the StreamInfo object.

for stream in streams: 
    print(stream)
#resolve_streams returned a list of stream objects. We then expanded those stream objects
#into lists to easily see more detail. The above for loop prints this expanded list for each stream. 

for stream in streams:
    if stream[1] == 'EEG':
        EEGStreamInfo = stream[2] #finds the StreamInfo object of the EEG stream
        break

print(EEGStreamInfo)

streamIn = pylsl.StreamInlet(EEGStreamInfo, max_buflen = 360, max_chunklen=0,recover=True)
print(streamIn)

#Okay, now the good stuff.

streamIn.open_stream() #This actually isn't required: pull_sample() and pull_chunk() implicitly open the stream.
#But it's good to be explicit because it makes the code clearer

print(streamIn.pull_sample()) #Returns a tuple with the actual values we want.
#The first element is the list of channel values, the second element is a timestamp. This is a snapshot of our stream
#at a certain point in time.

print(streamIn.pull_chunk()) #pulls a chunk of samples, i.e. multiple samples at once. idk yet how this works in terms of timing

#So this will likely be a matter of repeatedly calling one/both of the above two methods.
#Look at this to get a more thorough understanding: https://github.com/chkothe/pylsl/blob/master/pylsl/pylsl.py

#Uncomment the below line to see all the information about the stream, including relevant ports and channel labels:
#print(streamIn.info().as_xml())


#By the way, we indeed have to delete StreamInlet and StreamInfo objects ourselves (not quite in the same sense as what we do in C/C++
# but from our viewpoint it's the same: we just call a delete method).
#streamIn.__del__()
#EEGStreamInfo.__del__()
#Actually, these may throw errors: you can try uncommenting them to see if they work, but if they throw errors then no worries, just
#keep them commented. I probably missed a function that facilitates the deletion, or maybe it happens implicitly
