import RPi.GPIO as GPIO
#import src.environment as environment

# motorPin1 = 35
# motorPin2 = 33
motorPinE = 31

GPIO.setmode(GPIO.BOARD)
# GPIO.setup(motorPin1, GPIO.OUT)
# GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motorPinE, GPIO.OUT)

# GPIO.output(motorPin1,GPIO.HIGH)
pwmMotor = GPIO.PWM(motorPinE, 50)

pwmMotor.start(0)

def changeMotorSpeed(speed):
	#fanSpeed = environment.settings["fanSpeed"]
	fanSpeed=speed
	if fanSpeed == None:
		pwmMotor.ChangeDutyCycle(0)
		print("Fan is turned off")
	else:
		pwmMotor.ChangeDutyCycle(fanSpeed * 20)
		print("Fan speed is set to ",fanSpeed) 