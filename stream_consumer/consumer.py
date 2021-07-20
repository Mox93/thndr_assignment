import paho.mqtt.client as mqtt

from requests import post
from json import loads

from settings import settings


# The callback for when the client receives a CONNECT response from the server.
def on_connect(client_, userdata, rc, properties=None):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client_.subscribe(settings().mqtt_topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client_, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    try:
        post(settings().api_url, json=loads(msg.payload))
    except Exception as e:
        print("!!!", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings().mqtt_host, settings().mqtt_port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
