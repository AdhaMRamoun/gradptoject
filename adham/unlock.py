import hashlib
import mmap
import serial
import datetime
import os


hash_dict = {}

# Open the file and read its contents into a dictionary
with open(r'C:\Users\adham\OneDrive\Desktop\GradProject\adham\data.txt', 'r') as f:
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
            print("Access Granted for", username)
            current_time = datetime.datetime.now()
            print("Time of Entry:", current_time)
            if hash_dict[username][1][0] == '1':
                # remove the user from data.txt
                with open('data.txt', 'r') as f:
                    lines = f.readlines()
                with open('data.txt', 'w') as f:
                    for line in lines:
                        if not line.startswith(username):
                            f.write(line)
                print("User removed from data.txt")
            ser.write(b'1') # send '1' to the Arduino to turn on the green LED
        else:
            print("Access Denied")
            ser.write(b'0') # send '0' to the Arduino to turn on the red LED
