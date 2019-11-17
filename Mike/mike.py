import numpy as np
import matplotlib as plt
from pylsl import StreamInlet, resolve_byprop, StreamInfo, local_clock, StreamOutlet
import ble2lsl
from ble2lsl.devices import muse2016
from pprint import pprint
import time

def testing():
        dummy_streamer = ble2lsl.Dummy(muse2016) #

        streams = resolve_byprop("type", "EEG", timeout=5) #type: EEG, minimum return streams = 1, timeout after 5 seconds

        streamIn = StreamInlet(streams[0], max_chunklen = 12, recover = True) #Grab first stream from streams, MUSE chunk 12, drop lost stream
        print(streamIn)
        print(streamIn.info().channel_count())
        streamIn.open_stream() #This actually isn't required: pull_sample() and pull_chunk() implicitly open the stream.
        #But it's good to be explicit because it makes the code clearer
        print("Pull Sample")
        print(streamIn.pull_sample()) #Returns a tuple with the actual values we want.
        #The first element is the list of channel values, the second element is a timestamp. This is a snapshot of our stream
        #at a certain point in time.
        print("Pull Chunk")
        ts = time.time()
        while(1):
            x = streamIn.pull_chunk()
            if all(x):
            #if not np.shape(x) == (2, 0):
                print(np.shape(x))
                print(np.shape(x[1]))
                t = [t - ts for t in x[1]]
                print(t)
                print(t[-1]-t[0])

            # for y in x:
            #     for z in y:
            #         print(z)
                #print("\n")


        plt.style.use('ggplot')



            # data first then time stamps, sick

        pprint(streamIn.info().as_xml()) #what
        timeC = streamIn.time_correction()
        print(timeC)



        #Clean up time


        streams.clear()
        streamIn.close_stream() #calls lsl_close_stream
        streamIn.__del__() #Not throwing errors
        dummy_streamer.stop()




def main():
    print('''
  ____          _____ _  ________ _   _ _____
 |  _ \\   /\\   / ____| |/ /  ____| \\ | |  __ \\
 | |_) | /  \\ | |    | ' /| |__  |  \\| | |  | |
 |  _ < / /\\ \\| |    |  < |  __| | . ` | |  | |
 | |_) / ____ \\ |____| . \\| |____| |\\  | |__| |
 |____/_/    \\_\\_____|_|\\_\\______|_| \\_|_____/


    ''') #Everyone needs a distraction at some point...
    while(1):
        x = input("What do?:\n1. Test\n2. Quit\n")
        if (int(x) == 1 ):
            testing()
        else:
            print("As Julia would say: 'Cheers'")
            exit()


if __name__ == "__main__":
    main()

#Mo Called me an "Adept Coder" #IMadeItMom


def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1
