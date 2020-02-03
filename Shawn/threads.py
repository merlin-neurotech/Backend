import threading


def runFunc(functionToRun, argsToRun=None):
    if argsToRun:
        func = threading.Thread(target=functionToRun, kwargs=argsToRun)
    else:
        func = threading.Thread(target=functionToRun)
    func.run()
