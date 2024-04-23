import paho.mqtt.client as mqtt
import src.environment as environment
from decouple import config

def on_connect(client, userdata, flags, reason_code, propertiesc):
    print("Connected to MQTT broker")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

def mqttSetup():
    environment.mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    environment.mqttClient.on_connect = on_connect
    environment.mqttClient.on_disconnect = on_disconnect
    environment.mqttClient.connect(config('MQTT_BROKER_HOST'), int(config('MQTT_BROKER_PORT')), 60)
    environment.mqttClient.loop_forever()