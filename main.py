
from time import sleep
import urequests as requests
import ujson
import network
import socket
from machine import Pin, ADC
import machine

# Initialize ADC and analog pin for MQ-135 sensor
analog_pin_gas = ADC(Pin(26))

# Initialize buzzer pin
buzzer = Pin(27, Pin.OUT)

ssid = 'balsa'
password = 'dnsz7317'


firebase_url = "https://rpi1-5529c-default-rtdb.europe-west1.firebasedatabase.app/"
auth_token = "6qU01SWkIeIBhJwmKyn2UHknZXWC0q7CUe4RCWwY"

def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip, port=8080):
    # Open a socket
    address = (ip, port)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def get_device_id():
    id = ""
    for b in machine.unique_id():
        id += "{:02X}".format(b)
    return id
device_id = get_device_id()
def mainloop(connection):
    # Your main loop code here
    pass

def read_gas():
    # Read analog value from MQ-135 sensor
    analog_value_gas = analog_pin_gas.read_u16()
    
    # Convert analog value to gas concentration (adjust conversion formula based on sensor characteristics)
    gas_concentration = analog_value_gas  # Adjust conversion formula based on sensor characteristics

    return int(gas_concentration)  # Ensure the gas concentration is an integer

try:
    ip = connect()
    connection = open_socket(ip)
    mainloop(connection)
except KeyboardInterrupt:
    machine.reset()
    
    
while True:
    # Read gas concentration from sensor
    gas_concentration = read_gas()
    
    # Data to send to Firebase
    data = { "device_id": device_id,
             "gas_concentration": gas_concentration}
    json_data = ujson.dumps(data)

    # Construct URL for the Firebase endpoint
    endpoint = firebase_url + "baza.json"

    # If authentication token is provided, append it to the URL
    if auth_token:
        endpoint += "?auth=" + auth_token

    
    if gas_concentration > 8000:
        buzzer.on()  # Turn on the buzzer
    else:
        buzzer.off()  # Turn off the buzzer if gas concentration is below 2000

    # Make a POST request to Firebase
    response = requests.post(endpoint, data=json_data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Gas concentration data sent successfully to Firebase")
    else:
        print("Failed to send gas concentration data to Firebase:", response.status_code)

    # Close the response to free up resources
    response.close()

    # Wait for some time before sending the next data (adjust as needed)
    sleep(1)
