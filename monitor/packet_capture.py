import json
import subprocess
from time import sleep
import sys
import colorama


def progress_bar(value, endvalue, message, length=20):
    percent = float(value) / endvalue
    progress = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(progress))

    sys.stdout.write("\r{}: [{}] {}%".format(message, progress + spaces, int(round(percent * 100))))
    sys.stdout.flush()

colorama.init()

base_path = "/mas_data/packet/"
json_name = "config.json"

try:
    with open(base_path + json_name) as json_file:
        config = json.load(json_file)
except FileNotFoundError:
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: tcpdump config JSON not found.\n(Looked in {}{})".format(
        base_path, json_name) + colorama.Style.RESET_ALL)
    quit(-1)

# tcpdump = "/usr/sbin/tcpdump"
# interface = "vmnet8"
tcpdump = config["tcpdump"]
interface = config["interface"]
output_path = "/home/phil/Desktop/test1.cap"
vm_ip = "172.16.168.128"
print("Using tcpdump from \"{}\" on interface \"{}\" with VM IP \"{}\", and saving the output as \"{}\".".format(
    tcpdump, interface, vm_ip, output_path))
command = [tcpdump, "-q", "-n", "-i", interface, "-w", output_path, "host", vm_ip]
p = subprocess.Popen(command)

for i in range(0, 11):
    progress_bar(i, 10, "Waiting before terminating")
    sleep(1)

print("\nTerminating.")
try:
    p.terminate()
except Exception as e:
    print(colorama.Back.YELLOW + colorama.Fore.BLACK + "WARNING: failed to terminate tcpdump.\nException: {}".format(e)
          + colorama.Style.RESET_ALL)
