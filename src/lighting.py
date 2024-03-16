import RPi.GPIO as GPIO
#from gpiozero import RGBLED
#import src.environment as environment

redPin = 11
greenPin = 13
bluePin = 15


GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

pwmRed = GPIO.PWM(redPin, 50)
pwmGreen = GPIO.PWM(greenPin, 50)
pwmBlue = GPIO.PWM(bluePin, 50)

pwmRed.start(0)
pwmGreen.start(0)
pwmBlue.start(0)

def blink(pin):
    pin.ChangeDutyCycle(intensity)

def turnOff(pin):
	pin.ChangeDutyCycle(0)
        
def redOn():
	blink(pwmRed)
	
def greenOn():
	blink(pwmGreen)

def blueOn():
	blink(pwmBlue)
	
def warmOn():
	print("Warm on")
	blink(pwmRed)
	blink(pwmGreen)

def cyanOn():
	blink(pwmGreen)
	blink(pwmBlue)

def magentaOn():
	blink(pwmRed)
	blink(pwmBlue)

def whiteOn():
	blink(pwmRed)
	blink(pwmGreen)
	blink(pwmBlue)
	
def lightsOff():
	print("lightoff")
	turnOff(pwmRed)
	turnOff(pwmGreen)
	turnOff(pwmBlue)

def setLight(lightColor, lightIntensity):
	if(lightColor):
		global intensity
		intensity=lightIntensity
		print(intensity)
		if lightColor == "Red":
			redOn()
		elif lightColor == "Green":
			greenOn()
		elif lightColor == "Blue":
			blueOn()
		elif lightColor == "warm":
			warmOn()
		elif lightColor == "Cyan":
			cyanOn()
		elif lightColor == "Magenta":
			magentaOn()
		elif lightColor == "White":
			whiteOn()
	else:
		lightsOff()