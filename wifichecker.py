import json
import subprocess

def run(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print("error code 1")

def check_data():
    try:
        with open("pixelOS_data.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split(" : ")
                if key.strip() == "esp32wfiduyusizea" and value.strip() == "password5":
                    return True
            return False
    except FileNotFoundError:
        print("error code 3")
    except ValueError:
        print("error code 2")

# Check data
if check_data():
    run("esp32.py")

