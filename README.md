# Merlin Backend Repo

Whenever you achieve anything, upload it here.

### Current status:

We've figured out how to stream data and plot it in real time using PyQtGraph. We also have an understanding of the underlying data structures used in ble2lsl and pylsl

### Next Steps

Clean up the code and plan out the structure of the Working Title API. Implement that structure from end to end by offering plotting functionality.

Once the API structure has been designed and implemented (via a real-time time-domain plotting function), implement further features using this structure such as:
  - Non-Real Time (Offline) Implementation/Functionality
  - Transforms (PSD etc.)
  - Real Time Frequency Domain Plotting
  - Automated Feature Extraction
  - Pre-trained Classification Models
  - Etc.

Mike: research Multi processing/threading

Shawn: Put wrapper over current script

Cam: Bring white board markers, research multoprocessing/threading

Mo: Figure out linux support

Theo: research csv architecture

Sam: Come to a meeting, research with mike Multiprocessing/threading

Josh: Figure out python

### For Developers

Note to everyone: Usually, nobody knows what the clear next step is. Reading github code and comments is one of the best ways to proceed. Don't sit around waiting for somebody to tell you what to do, because nobody knows what to do.

If you don't already understand how ble2lsl and pylsl works, that's the first step: https://github.com/mohammadrashid0917/ble2lsl/blob/master/ble2lsl/ble2lsl.py,  https://github.com/chkothe/pylsl/blob/master/pylsl/pylsl.py

From there, investigate any of the other libraries/resources that are constantly being linked in the chat: looking into any of them and telling everyone else what you find will be productive.

We also need people who are willing to clean up code and implement scripts as data structures and functions
