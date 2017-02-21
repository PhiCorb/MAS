import json
import subprocess
from time import sleep
import sys


def progress_bar(value, endvalue, length=20):
    percent = float(value) / endvalue
    progress = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(progress))

    sys.stdout.write("\rWaiting before terminating: [{}] {}%".format(progress + spaces, int(round(percent * 100))))
    sys.stdout.flush()

base_path = "D:\\Phil Corbett\\Documents\\GitHub\\MAS\\monitor\\"
json_name = "config.json"

with open(base_path + json_name) as json_file:
    config = json.load(json_file)

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
    progress_bar(i, 10)
    sleep(1)

print("\nTerminating.")
p.terminate()  # TODO: move into try/except
