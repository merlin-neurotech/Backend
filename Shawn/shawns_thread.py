import threading
from PyQt5 import QtGui
import pylsl
import ble2lsl
from ble2lsl.devices import muse2016
from functions import plotTimeDomain

#https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/

########################
## Create a stream
########################
dummy_streamer = ble2lsl.Dummy(muse2016) #Using a dummy for now. We need some fuckin Muses. Why does most of the DEV TEAM not have any muses???


########################
## Find (Resolve) Stream
########################
streams = pylsl.resolve_byprop("type", "EEG", timeout=5) #type: EEG, minimum return streams = 1, timeout after 5 seconds
stream = streams[0]

# Start Threads
app = QtGui.QApplication([])
thread1 = threading.Thread(target=plotTimeDomain, args=(stream, 12), daemon=True)

thread2 = threading.Thread(target=plotTimeDomain, args=(stream, 12), daemon=True)

thread1.start()
thread2.start()