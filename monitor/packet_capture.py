import json
import subprocess
from time import sleep
import colorama
import os
from misc.progress_bar import progress_bar

colorama.init()
p = None


def start_capture(vm_ip, output_path):
    global p
    # base_path = "/mas_data/packet/"
    base_path = os.path.dirname(os.path.realpath(__file__))
    json_name = "/config.json"

    try:
        with open(base_path + json_name) as json_file:
            config = json.load(json_file)
    except FileNotFoundError:
        print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: tcpdump config JSON not found.\n(Looked in {}{})"
                                                        "".format(base_path, json_name) + colorama.Style.RESET_ALL)
        return -1

    # tcpdump = "/usr/sbin/tcpdump"
    # interface = "vmnet8"
    tcpdump = config["tcpdump"]
    interface = config["interface"]
    # output_path = "/home/phil/Desktop/test1.cap"
    # vm_ip = "172.16.168.128"
    print("Using tcpdump from \"{}\" on interface \"{}\" with VM IP \"{}\", and saving the output as \"{}\".".format(
        tcpdump, interface, vm_ip, output_path))
    command = [tcpdump, "-q", "-n", "-i", interface, "-w", output_path, "host", vm_ip]
    p = subprocess.Popen(command)
    return 0

# for i in range(0, 11):
#     progress_bar(i, 10, "Waiting before terminating")
#     sleep(1)


def end_capture():
    global p
    print("\nTerminating.")
    try:
        p.terminate()
        return 0
    except Exception as e:
        print(colorama.Back.YELLOW + colorama.Fore.BLACK + "WARNING: failed to terminate tcpdump.\nException: {}"
                                                           "".format(e) + colorama.Style.RESET_ALL)
        return -1

if __name__ == "__main__":
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: this is not intended to be executed directly!" +
          colorama.Style.RESET_ALL)
    exit(1)
