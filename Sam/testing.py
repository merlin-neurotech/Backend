import threading
from PyQt5 import QtGui
import pylsl
import ble2lsl
from ble2lsl.devices import muse2016
import functions
from StreamStaff import getStream_info
import time

def thread_test():
    streamer = ble2lsl.Dummy(muse2016)
    info = getStream_info(muse2016)
    runFunc(
    streamer.stop()


def fft_test(): #dont need a thread as the threading is in the backend (of course)
    stream = ble2lsl.Dummy(muse2016)
    info_ = getStream_info(muse2016)
    functions.fft(info_, output_stream_name='test_stream')
    stream.stop()

thread_test()
#thread = threading.Thread(target= thread_test)
#thread.start()

#time.sleep(20)
#thread._stop()
