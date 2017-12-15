import time

def autoSlide(refTextEdit):
    foo = refTextEdit.verticalScrollBar()
    foo.setValue(foo.maximum())

def getTime():
    actualTime = time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S")
    return actualTime