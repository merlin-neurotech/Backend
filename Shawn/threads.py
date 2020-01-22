import threading


def runFunc(functionToRun, argsToRun=None):
    if argsToRun:
        func = threading.Thread(target=functionToRun, args=(argsToRun,))
    else:
        func = threading.Thread(target=functionToRun)
    func.start()
