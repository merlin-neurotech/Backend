import ble2lsl
from ble2lsl.devices import muse2016 # Why do I have to import this seperately? This is dumb
import pylsl
import matplotlib.pyplot as plt
import numpy as np
from functions import live_plotter

#############################################
## Variables
#############################################
# Input Variables
FS = 256 # Sampling Rate of signal
TIMEWIN = 10 # Width of X-Axis in seconds (no fractions please)
CHUNKWIDTH = 12 # Number of samples in each chunk
CHANNELS=1 # Number of channels to stream

# Don't change these ones yet bc it messes with things
TICKFACTOR = 2 # Number of x-label ticks to have per second (eg 2 -> 0,2,4,6)

# Calculated Variables

XWIN = TIMEWIN*FS # Width of X-Axis in samples
XTICKS = (int)((TIMEWIN + 1)/TICKFACTOR) # Number of labels to have on X-Axis
CHUNKPERIOD = CHUNKWIDTH*(1/FS) # The length of each chunk in seconds

############################################
## Set Up
############################################
plt.style.use('ggplot') # use ggplot style for more sophisticated visuals

(x_vec, step) = np.linspace(0,TIMEWIN,XWIN+1, retstep=True) # vector used to plot y values
#xlabels = [ x * TICKFACTOR for x in list(range(-XTICKS, 0))] # Initialize x-labels
xlabels = np.zeros(XTICKS).tolist()
xticks = [ x * TICKFACTOR for x in list(range(0, XTICKS))] # Initialize locations of x-labels
y_vec = np.zeros((CHANNELS,len(x_vec))) # Initialize y_values as zero

# Initialize figure and subplots
fig = plt.figure(figsize=(13,6)) # Initialize figure

# Initialize subplots and lines
axes = []
lines = []
for i in range(0, CHANNELS):
    ax = fig.add_subplot(CHANNELS, 1, i+1)
    axes.append(ax) # Create list of axes/subplots
    line = ax.plot(x_vec,y_vec[i],alpha=0.8) # Returns a list with one line in it
    lines.append(line[0]) # Create list of lines


########################
## Create a stream
########################

dummy_streamer = ble2lsl.Dummy(muse2016) #Using a dummy for now. 

########################
## Find (Resolve) Stream
########################
streams = [stream for stream in pylsl.resolve_streams(wait_time=2)] # Get list of streamInfo Objects

for stream in streams:
    if (stream.type() == 'EEG'):
        EEGstream = stream

print('\nChannels: ', EEGstream.channel_count())

####################################################
## Create Stream Inlet to Accept Data
####################################################
streamIn = pylsl.stream_inlet(EEGstream, max_chunklen=12)
streamIn.open_stream()

###################################################
## Plotting Loop
###################################################
firstUpdate = True
while True:
    chunk = streamIn.pull_chunk()
    #rand_val = np.random.randn(1) # Get Random values for now
    #y_vec[-1] = rand_val # Append random value for now

    if np.shape(chunk) == (2, CHUNKWIDTH):
        chunkdata = np.transpose(chunk[0]) # Get chunk data and transpose to be CHANNELS x CHUNKLENTH
        xticks = [x - CHUNKPERIOD for x in xticks]
        #xticks = [x - step for x in xticks]  # Adjust locations of labels as 
        if(xticks[0] < 0): # Check if a label has crossed to the negative side of the y-axis
            # Delete label on left of x-axis and add a new one on the right side
            xticks.pop(0)
            xticks.append(xticks[-1] + TICKFACTOR)
            # Adjust time labels accordingly
            if (firstUpdate == False): # Check to see if it's the first update, if so skip so that time starts at zero
                xlabels.append(xlabels[-1] + TICKFACTOR)
                xlabels.pop(0)
            else:
                firstUpdate = False
        
        for i in range(0,CHANNELS):
            y_vec[i] = np.append(y_vec[i], chunkdata[i], axis=0)[len(chunkdata[i]):] # Append chunk to the end of y_data (currently only doing 1 channel)
            #y_vec[i] = y_vec[i][len(chunkdata[0]):] # Remove chunk from beginning
            
            lines[i] = live_plotter(x_vec, y_vec[i], lines[i], axes[i], xlabels, xticks, identifier='EEG Data', pause_time=CHUNKPERIOD/CHANNELS - 0.02) # Plot/Updata plotted data
            # Check if figure has been closed and end for loop
            if not plt.fignum_exists(fig.number):
                break

    #y_vec = np.append(y_vec[1:],0.0)
    
    # Check if figure has been closed and end infinite loop if so
    if not plt.fignum_exists(fig.number):
        break

dummy_streamer.stop()