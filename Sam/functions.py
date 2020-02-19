import pyqtgraph as pg
import numpy as np
from PyQt5 import QtGui
from pylsl import StreamInlet, StreamOutlet, StreamInfo, resolve_byprop
import threading

def fft_backend(input_stream, output_stream, window_length=256, pow2=True, window_type=np.hamming):
    
    #################################
    ## Stream Inlet and Outlet Creation
    #################################

    #streams = resolve_byprop("name",input_stream.name(),timeout= 10)
    #input_stream = streams[0]
    print(input_stream.channel_count())
    print(input_stream)
    print(input_stream.name())
    inlet = StreamInlet(input_stream, max_chunklen=12, recover=True)
    inlet.open_stream() # Stream is opened implicitely on first call of pull chunk, but opening now for clarity

    # Create StreamOutlet to push data to output stream
    outlet = StreamOutlet(output_stream)
    ###################################
    ## FFT
    ###################################
    
    buffer = np.empty((0,5))
    window = window_type(window_length)
    while(True):
        input_chunk = inlet.pull_chunk() # Pull Chunk
        #print(np.shape(input_chunk))

        if input_chunk[0] and np.shape(input_chunk)[1] > 0: # Check for available chunk
            #print("output samples")
            buffer = np.append(buffer, input_chunk[0], axis=0)

            if (len(buffer) >= window_length):
                # Take data from buffer
                data = buffer[0:window_length]
                data = np.transpose(data)

                # Get frequency labels/bins
                freq_labels = np.fft.rfftfreq(window_length, 1/input_stream.nominal_srate())

                # Take FFT of data for each channel
                data_windowed = []
                data_fft = []
                psd = []
                for i in range(0, output_stream.channel_count()):
                    # Multiply data by window
                    data_windowed.append(data[i] - np.mean(data[i], axis=0))
                    data_windowed[i] = data_windowed[i] * window

                    # Get FFT
                    data_fft.append(np.fft.rfft(data_windowed[i], n=window_length, axis=0))
                    data_fft[i] = data_fft[i]/window_length

                    # Convert FFT to PSD
                    psd.append(abs(data_fft[i])) # Take absolute value
                    # Assume input signal is real-valued and double power to account for negative frequencies 
                    # DC power (psd[i][0]) only occurs once and does not need to be doubled)
                    psd[i][1:] = 2*psd[i][1:]

                # Create Output Data Packet in shape 2 x N (Where N is the # of discrete frequencies)
                # The first dimension of output sample contains the data of shape CHANNELS x N
                # The second dimension contains the N labels for the frequencies in Hz 
                psd = np.transpose(psd)
                psd = psd.tolist()
                freq_labels = freq_labels.tolist()
                output_sample = (psd, freq_labels)
                #print(np.shape(output_sample))
                print(output_sample[0])

                # Push fft transform for each channel using outlet
                outlet.push_chunk(output_sample)



def fft(input_stream, output_stream_name='default', window_length=256, pow2=True, window_type=np.hamming, channels=0):

    #################################
    ## Create New Output StreamInfo Objectcd 
    #################################

    # Set Default Output Stream Name
    if (output_stream_name == 'default'):
        output_stream_name = str(input_stream.name() + '-PSD')

    # Get number of channels to transform
    if(channels == 0):
        channels = input_stream.channel_count() # Get number of channels

    # Create Output StreamInfo Object
    output_stream = StreamInfo(name=output_stream_name, 
        type='PSD', 
        channel_count=channels, 
        nominal_srate=input_stream.nominal_srate(),
        channel_format='float32',
        source_id=input_stream.source_id())

    ####################################
    ## Create Thread to Run fft_backend
    ####################################
    #fft_backend(input_stream, output_stream)

    # Currently if you run function in a diff thread it does not work
    thread = threading.Thread(target=fft_backend, 
        kwargs=dict(input_stream=input_stream, 
            output_stream=output_stream, 
            window_length=window_length, 
            pow2=pow2,
            window_type=window_type))

    thread.start()

    return output_stream


def plotTimeDomain(stream_info, chunkwidth=0, fs=0, channels=0, timewin=50, tickfactor=5, size=(1500, 800), title=None):
    """Plot Real-Time domain in the time domain using a scrolling plot.

    Accepts a pylsl StreamInlet Object and plots chunks in real-time as they are recieved
    using a scrolling pyqtgraph plot. Can plot multiple channels.

    Args:
        stream_info (pylsl StreamInfo Object): The stream info object for the stream to be plotted
        chunkwidth (int): The number of samples in each chunk when pulling chunks from the stream
        fs (int): The sampling frequency of the device. If zero function will attempt to determine 
            sampling frequency automatically
        channels (int): The number of channels in the stream (Eg. Number of EEG Electrodes). If
            zero the function will attempt determine automatically
        timewin (int): The number seconds to show at any given time in the plot. This affects the speed 
            with which the plot will scroll accross the screen. Can not be a prime number.
        tickfactor (int): The number of seconds between x-axis labels. Must be a factor of timewin
        size (array): Array of type (width, height) of the figure
        title (string): Title of the plot figure
    
    Returns:
        bool: True if window was closed and no errors were encountered. False if an error was encountered within
            the function
    """
    #################################
    ## Stream Inlet Creation
    #################################
    #stream = resolve_byprop("name",stream_info.name(),timeout= 10)
    inlet = StreamInlet(stream_info, max_chunklen=chunkwidth, recover=True)
    inlet.open_stream() # Stream is opened implicitely on first call of pull chunk, but opening now for clarity

    #################################
    ## Variable Initialization
    #################################

    ## Get/Check Default Params
    if(timewin%tickfactor != 0):
        print('''ERROR: The tickfactor should be a factor of of timewin. The default tickfactor
        \n is 5 seconds. If you changed the default timewin, make sure that 5 is a factor, or 
        \n change the tickfactor so that it is a factor of timewin''')
        return False

    if(fs == 0):
        fs = stream_info.nominal_srate() # Get sampling rate

    if(channels == 0):
        channels = stream_info.channel_count() # Get number of channels

    ## Initialize Constants
    XWIN = timewin*fs # Width of X-Axis in samples
    XTICKS = (int)((timewin + 1)/tickfactor) # Number of labels to have on X-Axis
    #CHUNKPERIOD = chunkwidth*(1/fs) # The length of each chunk in seconds

    ##################################
    ## Figure and Plot Set Up
    ##################################

    ## Initialize QT
    app = QtGui.QApplication([])

    ## Define a top-level widget to hold everything
    fig = QtGui.QWidget()
    fig.resize(size[0], size[1]) # Resize window
    if (title != None): 
        fig.setWindowTitle(title) # Set window title
    layout = QtGui.QGridLayout()
    fig.setLayout(layout)

    # Set up initial plot conditions
    (x_vec, step) = np.linspace(0,timewin,XWIN+1, retstep=True) # vector used to plot y values
    xlabels = np.zeros(XTICKS).tolist() # Vector to hold labels of ticks on x-axis
    xticks = [ x * tickfactor for x in list(range(0, XTICKS))] # Initialize locations of x-labels
    y_vec = np.zeros((channels,len(x_vec))) # Initialize y_values as zero

    # Set Up subplots and lines
    plots = []
    curves = []
    colors = ['c', 'm', 'g', 'r', 'y', 'b'] # Color options for various channels
    for i in range(0, channels):
        # Create axis item and set tick locations and labels
        axis = pg.AxisItem(orientation='bottom')
        axis.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]]) # Initialize all labels as zero
        # Create plot widget and append to list
        plot = pg.PlotWidget(axisItems={'bottom': axis}, labels={'left': 'Volts (mV)'}, title='Channel ' + (str)(i + 1)) # Create Plot Widget
        plot.plotItem.setMouseEnabled(x=False, y=False) # Disable panning for widget
        plot.plotItem.showGrid(x=True) # Enable vertical gridlines
        plots.append(plot)
        # Plot data and save curve. Append curve to list
        curve = plot.plot(x_vec, y_vec[i], pen=pg.mkPen(colors[i%len(colors)], width=0.5)) # Set thickness and color of lines
        curves.append(curve)
        # Add plot to main widget
        layout.addWidget(plot, i, 0)

    # Display figure as a new window
    fig.show()

    ###################################
    # Real-Time Plotting Loop
    ###################################

    firstUpdate = True
    while(True):
        chunk = inlet.pull_chunk()

        # (something is wierd with dummy chunks, get chunks of diff sizes, data comes in too fast)
        if chunk and np.shape(chunk)[1] > 0: # Check for available chunk 
            print(np.shape(chunk))
            chunkdata = np.transpose(chunk[0]) # Get chunk data and transpose to be CHANNELS x CHUNKLENTH
            chunkperiod = len(chunkdata[0])*(1/fs)
            xticks = [x - chunkperiod for x in xticks] # Update location of x-labels

            # Update x-axis locations and labels
            if(xticks[0] < 0): # Check if a label has crossed to the negative side of the y-axis

                # Delete label on left of x-axis and add a new one on the right side
                xticks.pop(0)
                xticks.append(xticks[-1] + tickfactor)

                # Adjust time labels accordingly
                if (firstUpdate == False): # Check to see if it's the first update, if so skip so that time starts at zero
                    xlabels.append(xlabels[-1] + tickfactor)
                    xlabels.pop(0)
                else:
                    firstUpdate = False
            
            # Update plotted data
            for i in range(0,channels):
                y_vec[i] = np.append(y_vec[i], chunkdata[i], axis=0)[len(chunkdata[i]):] # Append chunk to the end of y_data (currently only doing 1 channel)
                curves[i].setData(x_vec, y_vec[i]) # Update data

                # Update x-axis labels
                axis = plots[i].getAxis(name='bottom')
                axis.setTicks([[(xticks[i],str(xlabels[i])) for i in range(len(xticks))]])
               
        # Update QT Widget to reflect the changes we made
        pg.QtGui.QApplication.processEvents()

        # Check to see if widget if has been closed, if so exit loop
        if not fig.isVisible():
            break
    
    # Close the stream inlet
    inlet.close_stream()
    
    return True


def plotFreqDomain(stream_info, chunkwidth, channels=0, size=(1500, 1500), title=None):
    """Plot Real-Time in the frequency domain using a static x-axis and changing y axis values.

    Accepts a pylsl StreamInlet Object and plots chunks in real-time as they are recieved
    using a pyqtgraph plot. Can plot multiple channels.

    Args:
        stream_info (pylsl StreamInfo Object): The stream info object for the stream to be plotted
        chunkwidth (int): The number of samples in each chunk when pulling chunks from the stream
        fs (int): The sampling frequency of the device. If zero function will attempt to determine 
            sampling frequency automatically
        size (array): Array of type (width, height) of the figure
        title (string): Title of the plot figure
    
    Returns:
        bool: True if window was closed and no errors were encountered. False if an error was encountered within
            the function
    """
    #################################
    ## Stream Inlet Creation
    #################################
    inlet = StreamInlet(stream_info, max_chunklen=chunkwidth, recover=True)
    inlet.open_stream() # Stream is opened implicitely on first call of pull chunk, but opening now for clarity

    #################################
    ## Variable Initialization
    #################################

    if(channels == 0):
        channels = stream_info.channel_count() # Get number of channels

    ##################################
    ## Figure and Plot Set Up
    ##################################

    ## Initialize QT
    app = QtGui.QApplication([])

    ## Define a top-level widget to hold everything
    fig = QtGui.QWidget()
    fig.resize(size[0], size[1]) # Resize window
    if (title != None): 
        fig.setWindowTitle(title) # Set window title
    layout = QtGui.QGridLayout()
    fig.setLayout(layout)

    # Set up initial plot conditions
    (x_vec, step) = np.linspace(0,chunkwidth,chunkwidth, retstep=True) # vector used to plot y values
    y_vec = np.zeros((channels,len(x_vec))) # Initialize y_values as zero

    # Set Up subplots and lines
    plots = []
    curves = []
    colors = ['c', 'm', 'g', 'r', 'y', 'b'] # Color options for various channels
    for i in range(0, channels):
        # Create plot widget and append to list
        plot = pg.PlotWidget(labels={'left': 'Power (dB)'}, title='Channel ' + (str)(i + 1)) # Create Plot Widget
        plot.plotItem.setMouseEnabled(x=False, y=False) # Disable panning for widget
        plot.plotItem.showGrid(x=True) # Enable vertical gridlines
        plots.append(plot)
        # Plot data and save curve. Append curve to list
        curve = plot.plot(x_vec, y_vec[i], pen=pg.mkPen(colors[i%len(colors)], width=0.5)) # Set thickness and color of lines
        curves.append(curve)
        # Add plot to main widget
        layout.addWidget(plot, np.floor(i/2), i%2)

    # Display figure as a new window
    fig.show()

    ###################################
    # Real-Time Plotting Loop
    ###################################

    firstUpdate = True
    while(True):
        chunk = inlet.pull_chunk()

        if np.shape(chunk) == (2, chunkwidth): # Check for available chunk
            chunkdata = np.transpose(chunk[0]) # Get chunk data and transpose to be CHANNELS x CHUNKLENGTH

            # Update plotted data
            for i in range(0,channels):
                curves[i].setData(x_vec, chunkdata[i]) # Update data
               
        # Update QT Widget to reflect the changes we made
        pg.QtGui.QApplication.processEvents()

        # Check to see if widget if has been closed, if so exit loop
        if not fig.isVisible():
            break
    
    # Close the stream inlet
    inlet.close_stream()
    
    return True

