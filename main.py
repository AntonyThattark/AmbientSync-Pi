import RPi.GPIO as GPIO
from src.handler import makeAPIRequest 
from src.lighting import setLight
from src.fan import changeMotorSpeed
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
roomID = '1'

def getRoomInfo():
    return makeAPIRequest("GET", "/rooms/" + roomID + "/settings")

def updateUserScan(user):
    return makeAPIRequest("PUT", "/rooms/" + roomID + "/users/" + user + "/scan")

def setToPreferences(roomInfo):
    # environment.occupants = roomInfo["occupants"]
    # environment.settings = roomInfo["settings"]
    setLight(roomInfo[0]['light_color'],roomInfo[0]['light_intensity'])
    # checkTemperatureAndHumidity()
    changeMotorSpeed(roomInfo[0]['fan_speed'])

try:
    roomInfo = getRoomInfo()
    #mqttSubscriberThread.start()
    if roomInfo != {}:
        #environment.mqttClient.on_message = refreshPreferences
        setToPreferences(roomInfo)
        #changeSubscription()
        #printRoomInfo()
        #weatherCheckThread.start()
        #displayThread.start()
    while True:
        print("Scanner ready to scan. You may scan now")
        #scanAwait()
        user = scanUserAndReturnRoomInfo()
        roomInfo = updateUserScan(user)
        if roomInfo != {}:
            #scanSuccess()
            # if user in environment.occupants:
            #     displayMessage("Goodbye "+user + "!")
            # else:
            #     displayMessage("Welcome to the room "+user + "!")
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