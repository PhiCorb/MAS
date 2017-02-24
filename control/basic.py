import colorama
import json
import os
from time import sleep
import monitor.packet_capture as packet_capture
import monitor.pcap_parser as pcap_parser
import monitor.vm_control as vm_control
import misc.progress_bar

colorama.init()

base_path = os.path.dirname(os.path.realpath(__file__))
json_name = "/config.json"

try:
    with open(base_path + json_name) as json_file:
        config = json.load(json_file)
except FileNotFoundError:
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: Config JSON not found.\n(Looked in {}{})".format(
        base_path, json_name) + colorama.Style.RESET_ALL)
    quit(-1)
sample_root = config["sample_root"]
vm_root = config["vm_root"]
capture_root = config["capture_root"]

while True:
    sample_filename = input("Sample must be located in \"{}\"\nPlease enter the filename: ".format(sample_root))
    try:
        extension = os.path.splitext(sample_root + sample_filename)[1]
        break
    except FileNotFoundError:
        print(colorama.Back.YELLOW + colorama.Fore.BLACK + "File not found - please retry." + colorama.Style.RESET_ALL)
if extension == ".exe" or extension == ".msi":
    executable = True
else:
    executable = False
with open(sample_root + "config.json", "w") as json_file:
    (json.dump({"executable": executable, "filename": sample_filename}, json_file, indent=4))

vm_path = vm_root + "XP VM 1/XP VM 1.vmx"
vm_control.spawn_vm(vm_path)
packet_capture.start_capture("172.16.168.128", capture_root + "cap.pcap")

for i in range(0, 31):
    misc.progress_bar.progress_bar(i, 30, "Waiting before terminating")
    sleep(1)

packet_capture.end_capture()
vm_control.end_vm(vm_path)
vm_control.restore_vm(vm_path, "Snapshot")

pcap_parser.cap_dns(capture_root + "cap.pcap")
pcap_parser.cap_http(capture_root + "cap.pcap")
