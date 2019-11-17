import ble2lsl
from ble2lsl.devices import muse2016 # Why do I have to import this seperately? This is dumb
import pylsl
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from functions import liveQtPlotter

#############################################
## Variables
#############################################
# Input Variables
FS = 256 # Sampling Rate of signal
TIMEWIN = 50 # Width of X-Axis in seconds (no fractions please)
CHUNKWIDTH = 12 # Number of samples in each chunk
CHANNELS=3 # Number of channels to stream

# Don't change these ones yet bc it messes with things
TICKFACTOR = 5 # Number of x-label ticks to have per second (eg 2 -> 0,2,4,6)

# Calculated Variables

XWIN = TIMEWIN*FS # Width of X-Axis in samples
XTICKS = (int)((TIMEWIN + 1)/TICKFACTOR) # Number of labels to have on X-Axis
CHUNKPERIOD = CHUNKWIDTH*(1/FS) # The length of each chunk in seconds

############################################
## Set Up
############################################
(x_vec, step) = np.linspace(0,TIMEWIN,XWIN+1, retstep=True) # vector used to plot y values
xlabels = np.zeros(XTICKS).tolist()
xticks = [ x * TICKFACTOR for x in list(range(0, XTICKS))] # Initialize locations of x-labels
y_vec = np.zeros((CHANNELS,len(x_vec))) # Initialize y_values as zero

## Start by initializing Qt
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
fig = QtGui.QWidget()
fig.setWindowTitle('EEG Data')
fig.resize(1500, 800)
layout = QtGui.QGridLayout()
fig.setLayout(layout)

# Initialize subplots and lines
plots = []
colors = ['c', 'm', 'g', 'r', 'y', 'b']
curves = []
for i in range(0, CHANNELS):
    # Create axis item and set tick locations and labels
    axis = pg.AxisItem(orientation='bottom')
    axis.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]]) # Initialize all labels as zero
    # Create plot widget and append to list
    plot = pg.PlotWidget(axisItems={'bottom': axis}, labels={'left': 'Volts (mV)'}, title='Channel ' + (str)(i + 1))
    plot.plotItem.setMouseEnabled(x=False, y=False)
    plot.plotItem.showGrid(x=True)
    plots.append(plot)
    # Plot data and save curve. Append curve to list
    curve = plot.plot(x_vec, y_vec[i], pen=pg.mkPen(colors[i%len(colors)], width=0.5))
    curves.append(curve)
    # Add plot to main widget
    layout.addWidget(plot, i, 0)

# Display figure as a new window
fig.show()

########################
## Create a stream
########################

dummy_streamer = ble2lsl.Streamer(muse2016) #Using a dummy for now.

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
streamIn = pylsl.stream_inlet(EEGstream, max_chunklen=12, recover = True)
streamIn.open_stream()

###################################################
## Plotting Loop
###################################################
firstUpdate = True
while(True):
    print(streamIn.samples_available())
    chunk = streamIn.pull_chunk()

    if np.shape(chunk) == (2, CHUNKWIDTH):
        chunkdata = np.transpose(chunk[0]) # Get chunk data and transpose to be CHANNELS x CHUNKLENTH
        xticks = [x - CHUNKPERIOD for x in xticks]

        # Update x-axis locations and labels
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

        # Update plotted data
        for i in range(0,CHANNELS):
            y_vec[i] = np.append(y_vec[i], chunkdata[i], axis=0)[len(chunkdata[i]):] # Append chunk to the end of y_data (currently only doing 1 channel)
            curves[i] = liveQtPlotter(x_vec, y_vec[i], curves[i], plots[i], xlabels, xticks) # Plot/Updata plotted data

    # Update QT Widget to reflect the changes we made
    pg.QtGui.QApplication.processEvents()

    # Check to see if widget if has been closed, if so exit loop
    if not fig.isVisible():
        break

dummy_streamer.stop()
