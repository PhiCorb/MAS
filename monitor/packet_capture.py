import subprocess
from time import sleep
import sys


def progress_bar(value, endvalue, length=20):
    percent = float(value) / endvalue
    progress = '#' * int(round(percent * length))
    spaces = ' ' * (length - len(progress))

    sys.stdout.write("\r\tWaiting before terminating: [{}] {}%".format(progress + spaces, int(round(percent * 100))))
    sys.stdout.flush()

tcpdump = "/usr/sbin/tcpdump"
interface = "vmnet8"
output_path = "~/test1.cap"
vm_ip = "172.16.168.128"
print("Using tcpdump from \"{}\" on interface \"{}\" with VM IP \"{}\", and saving the output as \"{}\".".format(
    tcpdump, interface, vm_ip, output_path))
command = [tcpdump, "-q", "-n", "-i", "v", interface, "-w", output_path, "host", vm_ip]
p = subprocess.Popen(command)

for i in range(0, 11):
    progress_bar(i, 10)
    sleep(1)

print("Terminating.")
p.terminate()  # TODO: move into try/except
