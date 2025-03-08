#!/usr/bin/python3.11

# ============================================
# code is placed under the MIT license
#  Copyright (c) 2023 J-M-L
#  For the Arduino Forum : https://forum.arduino.cc/u/j-m-l
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#  ===============================================


import sys, threading, queue, serial, time, pandas
import serial.tools.list_ports

baudRate = 115200
arduinoQueue = queue.Queue()
localQueue = queue.Queue()

class NoValidPortError(Exception):
    """Exception raised when no valid Arduino ports are found."""
    pass

def selectArduino():
    ports = serial.tools.list_ports.comports()
    valid_ports = [port for port in ports if port.hwid != 'n/a']  # Filter out ports with 'n/a' hwid
    
    if not valid_ports:
        raise NoValidPortError("No valid Arduino ports found.")  # Raise an error if no valid ports

    print('PORT\tDEVICE\t\t\tMANUFACTURER')
    for index, value in enumerate(sorted(valid_ports)):
        print(f"{index}\t{value.name}\t{value.manufacturer}")  # Display sorted list with index

    choice = -1
    while choice < 0 or choice >= len(valid_ports):
        answer = input("➜ Select your port: ")
        if answer.isnumeric():
            choice = int(answer)

    selectedPort = sorted(valid_ports)[choice]  # Map the user's choice to the filtered list
    print(f"selecting: {selectedPort.device}")
    return selectedPort.device

def listenToArduino():
    message = b''
    while True:
        incoming = arduino.read()
        if incoming == b'\n':
            try:
                arduinoQueue.put(message.decode('utf-8').strip().upper())
            except UnicodeDecodeError as e:
                # Handle the error: log it, ignore the message, or take other action
                print(f"UnicodeDecodeError: {e}. Message skipped.")
            message = b''
        else:
            if incoming not in (b'', b'\r'):
                message += incoming

def listenToLocal():
    while True:
        command = sys.stdin.readline().strip().upper()
        localQueue.put(command)

def configureUserInput():
    localThread = threading.Thread(target=listenToLocal, args=())
    localThread.daemon = True
    localThread.start()

def configureArduino():
    global arduinoPort
    arduinoPort = selectArduino()
    global arduino
    arduino = serial.Serial(arduinoPort, baudrate=baudRate, timeout=.1)
    arduinoThread = threading.Thread(target=listenToArduino, args=())
    arduinoThread.daemon = True
    arduinoThread.start()

# ---- CALLBACKS UPON MESSAGES -----

timestamps = []
temperatures = []
capacitives = []

def handleLocalMessage(lMessage):
    if lMessage.upper() == "REQUEST":
        arduino.write(lMessage.encode('utf-8'))
        arduino.write(bytes('\n', encoding='utf-8'))
    elif lMessage.upper() == "EXPORT":
        readableTimestamps = timestamps
        map(time.asctime, readableTimestamps)
        dict = {"timestamp": readableTimestamps, "temperature": temperatures, "capacitive": capacitives}
        df = pandas.DataFrame(data=dict)
        df.to_csv("sensorData.csv", header=False, index=False)
    else:
        print("Unknown message.")

def handleArduinoMessage(aMessage):
    pair = aMessage.split(":")
    if len(pair) != 2:
        return
    
    key = pair[0]
    value = pair[1]

    if key.startswith("TEMPERATURE"):
        temperatures.append(value)
    elif key.startswith("CAPACITIVE"):
        capacitives.append(value)

    if len(temperatures) == len(capacitives):
        timestamps.append(time.time())

# ---- MAIN CODE -----

configureArduino()                                      # will reboot AVR based Arduinos
configureUserInput()                                    # handle stdin 

print("Waiting for Arduino")

# --- A good practice would be to wait for a know message from the Arduino
# for example at the end of the setup() the Arduino could send "OK"
while True:
    if not arduinoQueue.empty():
        if arduinoQueue.get() == "OK":
            break
print("Arduino Ready")

# --- Now you handle the commands received either from Arduino or stdin
while True:
    if not arduinoQueue.empty():
        handleArduinoMessage(arduinoQueue.get())

    if not localQueue.empty():
        handleLocalMessage(localQueue.get())