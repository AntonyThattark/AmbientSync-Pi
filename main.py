import RPi.GPIO as GPIO
import time
import threading
import src.environment as environment
from src.handler import makeAPIRequest 
from src.lighting import setLight, lightsOff
from src.fan import changeMotorSpeed
from src.temperature import checkTemperatureAndHumidity
from src.subscriber import mqttSetup
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
roomID = '1'
global is_writing
is_writing = False

def getRoomInfo():
    return makeAPIRequest("GET", "/rooms/" + roomID + "/settings")

def updateUserScan(user):
    return makeAPIRequest("PUT", "/rooms/" + roomID + "/users/" + user + "/scan")

def scanUserAndReturnRoomInfo():
    global is_writing
    try:
        if not is_writing:            
            _, user = reader.read()
            print(user[0],"m")
            if(user!="" or user!=None or user!=" "):
                return user[0]
            else:
                return(scanUserAndReturnRoomInfo())            
        
        else:
            print("Hold tag near the module...")
            _, user = reader.read()
            print(user[0],"m")
            if(user!="" or user!=None or user!=" " or user!='\x00'):
                print("contains value")
                is_writing=False
                return ""
            for i in range (5):
                reader.write(is_writing)
            print("Written",is_writing)
            is_writing=False
            return ""

    except Exception as err:
        print("scanning error occured: ", err)
        return(scanUserAndReturnRoomInfo())

def setToPreferences(roomInfo):
    environment.temp = roomInfo[0]['room_temp']
    lightsOff()
    # environment.occupants = roomInfo["occupants"]
    # environment.settings = roomInfo["settings"]
    setLight(roomInfo[0]['light_color'],roomInfo[0]['light_intensity'])
    checkTemperatureAndHumidity()
    changeMotorSpeed(roomInfo[0]['fan_speed'])

def on_message(client, userdata, message):
    if(message.topic=="newUser"):
        global is_writing
        is_writing=message.payload.decode()
        writeUserIdToCard(message)
    if(message.topic=='preference/'+roomID):
        refreshPreferences(message)

def refreshPreferences(message):
    print("Message received from broker. Topic: ", message.topic, " Content:", message.payload.decode())
    roomInfo = getRoomInfo()
    setToPreferences(roomInfo)

def writeUserIdToCard(message):
    print("Message received from broker. Topic: ", message.topic, " Content:", message.payload.decode())

def weatherCheck():
    while True:
        time.sleep(60*1)
        checkTemperatureAndHumidity()

def changeSubscription():
    environment.mqttClient.subscribe('preference/'+roomID)
    environment.mqttClient.subscribe('newUser')

weatherCheckThread = threading.Thread(target=weatherCheck, daemon=True)
mqttSubscriberThread = threading.Thread(target=mqttSetup, daemon=True)

try:
    roomInfo = getRoomInfo()
    print(roomInfo)
    mqttSubscriberThread.start()
    time.sleep(0.5)
    if roomInfo != {}:
        environment.mqttClient.on_message = on_message
        setToPreferences(roomInfo)
        changeSubscription()
        weatherCheckThread.start()
    while True:
        print("Scanner ready to scan. You may scan now")
        #environment.mqttClient.on_message = refreshPreferences
        environment.mqttClient.on_message = on_message
        user = scanUserAndReturnRoomInfo()
        if(user!='\x00'):
            update = updateUserScan(user)
            if(update):
                roomInfo = getRoomInfo()
                if roomInfo != {}:
                    print(roomInfo)
                    #scanSuccess()
                    setToPreferences(roomInfo)
                    # changeSubscription()
                    # printRoomInfo()
                # else:
                #     scanFail()
        print("Wait till prompted other wise to scan again")
        time.sleep(2.5)
    
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as err:
    print("Unexpected error occured: ", err)
    GPIO.cleanup()