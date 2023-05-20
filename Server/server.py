import string
import secrets
import hashlib
import mmap
import os

symbols = ['*', '%', '£', '@', '#', '&', '!']  # Can add more

def register():
    username = input('Enter the username: ')
    password = input('Enter a password: ')
    re_enter_password = input('Re-Enter Your Password: ')
    while password != re_enter_password:
        print("Passwords do not match")
        password = input('Enter a password: ')
        re_enter_password = input('Re-Enter Your Password: ')
    password_hasher = hashlib.sha256()
    password = password.encode('utf-8')
    password_hasher.update(password)
    password_hasher.digest()
    password_hash = password_hasher.hexdigest()

    # Check if the data.txt file exists and is not empty
    if os.path.exists(r"C:\Users\adham\OneDrive\Desktop\GradProject\Server\data.txt") and os.stat(r"C:\Users\adham\OneDrive\Desktop\GradProject\Server\data.txt").st_size != 0:
        # Use mmap to prevent overwriting existing users
        with open(r'C:\Users\adham\OneDrive\Desktop\GradProject\Server\data.txt', 'a+') as f:
            s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            new_user = username.encode('utf-8')
            if s.find(new_user) != -1:
                print('User already exists')
                return None
    # If the file is empty or doesn't exist, just append the new user
    with open(r'C:\Users\adham\OneDrive\Desktop\GradProject\Server\data.txt', 'a') as f:
        pin = input('Enter a 4-digit PIN: ')
        rand_str = input('Enter a random string: ')  # User-entered random string
        data = f"{username},{password_hash},{hashlib.sha256((rand_str + pin).encode('utf-8')).hexdigest()}\n"
        f.write(data)
    print('User registered')
    return username, rand_str


def login(username, password):
    with open(r"C:\Users\adham\OneDrive\Desktop\GradProject\Server\data.txt", "r") as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[0].strip() == username:
                password_hash = parts[1]
                password_hasher = hashlib.sha256()
                password = password.encode('utf-8')
                password_hasher.update(password)
                password_hasher.digest()
                password_hash_calculated = password_hasher.hexdigest()
                if password_hash_calculated == password_hash:
                    print('Login successful')
                    return True
                else:
                    print('Incorrect password')
                    return False
        print('User not found')
        return False

def add_user_data_to_file(username, logged_in_user):
    with open('data.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[0].strip() == username:
                rand_str = parts[2].strip()
                break
        else:
            print('User not found')
            return
    
    folder_path = os.path.join("C:/Users/adham/OneDrive/Desktop/GradProject", logged_in_user)
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, "data.txt")
    with open(file_path, 'w') as f:
        f.write(f"{username},{rand_str},0000000000000000\n")
    print(f'Data saved to {file_path}')

def delete_user(username):
    with open("data.txt", "r") as f:
        lines = f.readlines()

    with open("data.txt", "w") as f:
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[0].strip() != username:
                f.write(line)
    
    folder_path = os.path.join("C:/Users/adham/OneDrive/Desktop/GradProject", username)
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        print(f'User {username} deleted')
    else:
        print(f'User {username} not found')

def update_timecontrol(username, timecontrol):
    folder_path = os.path.join("C:/Users/adham/OneDrive/Desktop/GradProject/", logged_in_user)
    file_path = os.path.join(folder_path, "data.txt")
    
    lines = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(file_path, "w") as f:
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) == 4 and parts[0].strip() == username:
                existing_timecontrol = parts[3].strip()
                if len(existing_timecontrol) >= 16:
                    updated_timecontrol = timecontrol + existing_timecontrol[1:]
                else:
                    updated_timecontrol = timecontrol.ljust(16, "0")
                f.write(f"{username},{parts[1]},{parts[2]},{updated_timecontrol}\n")
            else:
                f.write(line)

    print(f"Onetime access updated for user {username}")

choice = 1
logged_in = False
logged_in_user = ""

## Menu
while choice != '0':
    print('To Login Enter 1')
    print('To Register New User Enter 2')
    if logged_in:
        print('To Add User Enter 3')
        print('To Delete User Enter 4')
    print('To Exit Enter 0')
    choice = input()
    
    if choice == '1':
        username = input('Enter the username: ')
        password = input('Enter the password: ')
        if login(username, password):
            logged_in = True
            logged_in_user = username
            print('Login successful')

    elif choice == '2':
        if logged_in:
            print('You are already logged in')
        else:
            user, rand_str = register()
            if user:
                print(f'User registered. Your randomly generated code is {rand_str}')
    
    elif choice == '3':
        if logged_in:
            x = input('User to add: ')
            add_user_data_to_file(x, logged_in_user)
        else:
            print('Please login first')
    
    elif choice == '4':
        if logged_in:
            username = input('Enter the username to delete: ')
            delete_user(username)
        else:
            print('Please login first')

    elif choice == '5':
        if logged_in:
            username = input("Enter the username to change access to one time access: ")
            update_timecontrol(username, "1000000000000000")
        else:
            print("Please login first")


