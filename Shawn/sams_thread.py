import threading
from testPylsl import running

thread1 = threading.Thread(target= running)
thread1.start()

thread2 = threading.Thread(target= running)
thread2.start()
