import json
from time import sleep
import sys
import subprocess


def progress_bar(value, endvalue, length=20):
    percent = float(value) / endvalue
    progress = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(progress))

    sys.stdout.write("\r\tWaiting before execution: [{}] {}%".format(progress + spaces, int(round(percent * 100))))
    sys.stdout.flush()

base_path = "D:\\Phil Corbett\\Documents\\GitHub\\MAS\\guest\\"
json_name = "config.json"

with open(base_path + json_name) as json_file:
    config = json.load(json_file)

if config["exec"]:  # Sample can be executed with subprocess.call()
    print("Preparing to launch sample \"{}\".".format(config["sample"]))
    for i in range(0, 6):
        progress_bar(i, 5)
        sleep(1)
    subprocess.call(base_path + config["filename"], shell=True)

# TODO: Add guest execution code
