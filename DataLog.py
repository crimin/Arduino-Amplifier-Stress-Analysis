import sys
import datetime

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui

import serial
import numpy as np
from scipy.fft import fft

import serial.tools.list_ports
import threading
import queue

app = QtWidgets.QApplication(sys.argv)

class dataCollect(object):
    dataSet0 = queue.deque(maxlen=1000)

# ----------------------------------------------------
# Set log filename ONCE here
# ----------------------------------------------------
LOGFILE = "test.txt"
#endLoadCal4.txt
# ----------------------------------------------------
# Create/clear log file
# ----------------------------------------------------
def logData():
    with open(LOGFILE, 'w') as f:
        pass

# ----------------------------------------------------
# FFT helper
# ----------------------------------------------------
def fourier(column_data, captureFrequency):
    length = len(column_data)
    Y_mag = 2 * abs(fft(column_data)) / length
    Y = [Y_mag[i] for i in range(int(length/2)+1)]
    f = [(0.5*captureFrequency*i)/float(length/2) for i in range(int(length/2+1))]
    return (f, Y)

# ----------------------------------------------------
# PLOTS
# ----------------------------------------------------
p0 = pg.plot()
p0.disableAutoRange()
p0.setXRange(0,1000)
p0.setYRange(0,5)
p0.showGrid(x=True,y=True,alpha=1)
curve0 = p0.plot()


def updater0():
    curve0.setData(dataCollect.dataSet0, clear=True,pen='r')


# ----------------------------------------------------
# SERIAL CONNECTION
# ----------------------------------------------------
serialArduino = serial.Serial("/dev/ttyACM0", 9600)

logData()

# ----------------------------------------------------
# LOGGER — writes to LOGFILE
# ----------------------------------------------------
def getData1():
    while True:
        line = serialArduino.readline().decode('utf-8', errors='ignore').strip()

        try:
            adc = float(line)
        except:
            continue

        dataCollect.dataSet0.append(adc)

        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        with open(LOGFILE, 'a') as f:
            f.write(f"{ts}, {adc}\n")

# ----------------------------------------------------
# THREAD
# ----------------------------------------------------
thread0 = threading.Thread(target=getData1)
thread0.start()

# ----------------------------------------------------
# TIMERS FOR PLOTTING
# ----------------------------------------------------
timer0 = QtCore.QTimer()
timer0.timeout.connect(updater0)
timer0.start(10)