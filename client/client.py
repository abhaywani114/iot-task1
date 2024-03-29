import threading
import time
import random
import json
import socket

class IoTDevice(threading.Thread):
    def __init__(self, device_id, data_func, port):
        super().__init__()
        self.device_id = device_id
        self.data_func = data_func
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def generate_data(self):
        while True:
            data = self.data_func()
            timestamp = time.time()
            message = {'device_id': self.device_id, 'timestamp': timestamp, 'data': data}
            print("Sending" , message)
            json_message = json.dumps(message)
            self.socket.send(json_message.encode())
            time.sleep(1)  # Adjust the delay as needed

    def run(self):
        self.socket.connect(('localhost', self.port))
        self.generate_data()

def generate_2_digit_number():
    return random.randint(10, 99)

def generate_3_digit_number():
    return random.randint(100, 999)

def generate_4_digit_number():
    return random.randint(1000, 9999)

def generate_2_letters():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=2))

def generate_4_letters():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))

def concatenate_2_digit_number_and_2_letters():
    return str(generate_2_digit_number()) + generate_2_letters()

def concatenate_4_letters_and_4_digit_number():
    data_4_letters = generate_4_letters()
    data_4_digit_number = str(generate_4_digit_number())
    return data_4_letters + data_4_digit_number[-2:]

def main():
    PORT = 8888

    devices = [
        IoTDevice('D1', generate_2_digit_number, PORT),
        IoTDevice('D2', generate_3_digit_number, PORT),
        IoTDevice('D3', generate_4_digit_number, PORT),
        IoTDevice('D4', generate_2_letters, PORT),
        IoTDevice('D5', generate_4_letters, PORT),
        IoTDevice('D6', concatenate_2_digit_number_and_2_letters, PORT),
        IoTDevice('D7', concatenate_4_letters_and_4_digit_number, PORT)
    ]

    for device in devices:
        device.start()

if __name__ == "__main__":
    main()

