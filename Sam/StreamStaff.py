import pylsl as pl 

def getStream_info(device, max_cnhunk = 0, max_chunkln = 12, stream_type = 'EEG'):
    stream = pl.resolve_byprop('type', stream_type, timeout= 2)
    if len(stream) == 0:
        raise RuntimeError("no {} stream found".format(stream_type))
    print(type(stream))
    return stream[0]


    #threading will also be in this python file 
