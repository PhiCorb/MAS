import json
from time import sleep
import sys
import subprocess
import os
import colorama


def progress_bar(value, endvalue, message, length=20):
    percent = float(value) / endvalue
    progress = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(progress))

    sys.stdout.write("\r{}: [{}] {}%".format(message, progress + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def go():
    for i in range(0, 6):
        progress_bar(i, 5, "Waiting for files to be copied to share")
        sleep(1)
    print()

    # base_path = "C:\\mas_data\\"
    base_path = os.path.dirname(os.path.realpath(__file__))
    json_name = "\\config.json"

    try:
        with open(base_path + json_name) as json_file:
            config = json.load(json_file)
    except FileNotFoundError:
        print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: Guest config JSON not found.\n(Looked in {}{})".format(
            base_path, json_name) + colorama.Style.RESET_ALL)
        return -1

    share_path = config["share"]

    try:
        with open(share_path + json_name) as json_file:
            sample_config = json.load(json_file)
    except FileNotFoundError:
        print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: Sample config JSON not found.\n(Looked in {}{})".format(
            share_path, json_name) + colorama.Style.RESET_ALL)
        return -1

    if sample_config["executable"]:  # Sample can be executed with subprocess.call()
        print("Preparing to launch sample \"{}\".".format(sample_config["filename"]))
        for i in range(0, 6):
            progress_bar(i, 5, "Waiting before executing")
            sleep(1)
        print()
        subprocess.call(share_path + "\\" + sample_config["filename"], shell=True)
    else:
        print(colorama.Back.YELLOW + "Sample marked as not being executable using subprocess.call() - "
                                     "TODO: add alternatives." + colorama.Style.RESET_ALL)
if __name__ == "__main__":
    colorama.init()
    go()
