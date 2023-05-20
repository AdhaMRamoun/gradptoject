import hashlib
import mmap
import serial
from datetime import datetime
import os


hash_dict = {}

# Open the file and read its contents into a dictionary
with open('data.txt', 'r') as f:
    for line in f:
        name, hash_comp, limitations = line.strip().split(',')
        hash_dict[name] = (hash_comp, limitations)

ser = serial.Serial('COM3', 9600)  # change 'COM3' to the correct port name for your device

while True:
    if ser.in_waiting > 0:
        data = ser.readline().rstrip().decode('utf-8')  # read the data from serial port
        print("UID received:", data)
        pin = input('Enter the 4 digit pin: ')
        combination = data + pin
        m = hashlib.sha256()
        password = combination.encode('utf-8')
        m.update(password)
        x = m.hexdigest()
        if x in [v[0] for v in hash_dict.values()]:
            username = [k for k, v in hash_dict.items() if v[0] == x][0]
            x = datetime.today().weekday() +1
            current_time = datetime.datetime.now()
            hour = str(current_time.hour)
            min = str(current_time.minute)
            clock = hour+min
            opentime = hash_dict[username][1][0:5]
            closetime = hash_dict[username][1][0:5]

            if hash_dict[username][1][0] == '1':
                print("Access Granted for", username)
                current_time = datetime.now()
                print("Time of Entry:", current_time)
                ser.write(b'1') # send '1' to the Arduino to turn on the green LED
                with open('data.txt', 'r') as f:
                    lines = f.readlines()
                with open('data.txt', 'w') as f:
                    for line in lines:
                        if not line.startswith(username):
                            f.write(line)
                print("User removed from data.txt")
            elif hash_dict[username][1][x] == '1':
                print('You are not allowed on that day of the week')
                print("Access Denied")
                ser.write(b'0') # send '0' to the Arduino to turn on the red LED
            elif clock < opentime or clock > closetime:
                print('your working hours are between: ', opentime,' and ', closetime)
                print("Access Denied")
                ser.write(b'0') # send '0' to the Arduino to turn on the red LED
            else:
                print("Access Granted for", username)
                current_time = datetime.now()
                print("Time of Entry:", current_time)
                ser.write(b'1') # send '1' to the Arduino to turn on the green LED
