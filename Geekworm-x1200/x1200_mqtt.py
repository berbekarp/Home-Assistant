import smbus2 as smbus
import time
import json
import paho.mqtt.client as mqtt

# --- BEÁLLÍTÁSOK ---
MQTT_BROKER = "192.168.X.X"  # A Home Assistant / MQTT IP címe
MQTT_PORT = 1883
MQTT_USER = "A_TE_FELHASZNALOD"
MQTT_PASS = "A_TE_JELSZAVAD"
MQTT_TOPIC = "homeassistant/sensor/x1200/state"

I2C_ADDR = 0x36 # MAX17048 chip címe
I2C_BUS = 1     # Pi 5 I2C busz

def read_voltage(bus):
    try:
        read = bus.read_word_data(I2C_ADDR, 0x02)
        swapped = ((read & 0xFF) << 8) | (read >> 8)
        voltage = swapped * 78.125 / 1000000
        return round(voltage, 2)
    except:
        return 0.0

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Sikeresen csatlakozva az MQTT brókerhez!")
    else:
        print(f"Csatlakozási hiba, kód: {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

if MQTT_USER and MQTT_PASS:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

bus = smbus.SMBus(I2C_BUS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        payload = {
            "voltage": read_voltage(bus),
            "battery_percent": read_capacity(bus)
        }
        client.publish(MQTT_TOPIC, json.dumps(payload))
        time.sleep(30)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    bus.close()
