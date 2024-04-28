import Adafruit_DHT
import RPi.GPIO as GPIO
import src.environment as environment

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# heaterPin = 16
# coolerPin = 18

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(heaterPin, GPIO.OUT)
# GPIO.setup(coolerPin, GPIO.OUT)

def checkTemperatureAndHumidity():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None or temperature is not None:
        print("Current Temperature: ", temperature)
        print("Current Humidity: ", humidity)
        if(environment.temp==None):
            controlTemperature(0,0)
        else:
            controlTemperature(environment.temp, temperature)
    else:
        print("Sensor failure")

def controlTemperature(required, current):
    if required>current:
        print("heater on")
        # GPIO.output(heaterPin, GPIO.LOW)
        # GPIO.output(coolerPin, GPIO.HIGH)
    elif required<current:        
        print("cooler on")
        # GPIO.output(heaterPin, GPIO.HIGH)
        # GPIO.output(coolerPin, GPIO.LOW)
    else:
        print("A/C OFF")
        # GPIO.output(heaterPin, GPIO.HIGH)
        # GPIO.output(coolerPin, GPIO.HIGH)

#checkTemperatureAndHumidity()