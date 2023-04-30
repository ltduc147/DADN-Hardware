import serial.tools.list_ports
import time

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        print(strPort)
        if "USB-SERIAL" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort 
    # return "COM1"

Serial_port = getPort()
if Serial_port != "None":
    print(Serial_port)
    ser = serial.Serial( port=Serial_port, baudrate=115200)

mess = ""
def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    # Publish data to server
    if splitData[0] == "T":
        client.publish("ltduc147/feeds/temperature-sensor", splitData[1])
    if splitData[0] == "H":
        client.publish("ltduc147/feeds/humidity-sensor", splitData[1])
    if splitData[0] == "SM":
        client.publish("ltduc147/feeds/soil-moisture-sensor", splitData[1])

mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            time.sleep(1)
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


def writeCmd(cmd, topic):
    if topic == "ltduc147/feeds/semi-auto":
        print(str("0:"+cmd))
        ser.write(str("0:"+cmd).encode("utf-8"))
    if topic == "ltduc147/feeds/auto":
        print(str("1:"+cmd))
        print(len(cmd))
        ser.write(str("1:"+cmd).encode("utf-8"))
    if topic == "ltduc147/feeds/pump-switch":
        print(str("2:"+cmd))
        ser.write(str("2:"+cmd).encode("utf-8"))