import colorama
import json
import os
from time import sleep
import datetime
import monitor.packet_capture as packet_capture
import monitor.pcap_parser as pcap_parser
import monitor.vm_control as vm_control
import db.mongo
import misc.progress_bar
import misc.md5

colorama.init()
valid = False

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

while not valid:
    sample_filename = input("Sample must be located in \"{}\"\nPlease enter the filename: ".format(sample_root))
    valid = os.path.isfile(sample_root + sample_filename)
    if not valid:
        print(colorama.Back.YELLOW + colorama.Fore.BLACK + "File not found - please retry." + colorama.Style.RESET_ALL)
extension = os.path.splitext(sample_root + sample_filename)[1]
if extension == ".exe" or extension == ".msi":
    executable = True
else:
    executable = False
with open(sample_root + "config.json", "w") as json_file:
    (json.dump({"executable": executable, "filename": sample_filename}, json_file, indent=4))

misc.progress_bar.progress_bar(0, 1, "Calculating sample MD5")
md5 = misc.md5.file(sample_root + sample_filename)
misc.progress_bar.progress_bar(1, 1, "Calculating sample MD5")
print("\nSample MD5: {}".format(md5))

print("Spawning VM...")
vm_path = vm_root + "XP VM 1/XP VM 1.vmx"
vm_control.spawn_vm(vm_path)
packet_capture.start_capture("172.16.168.128", capture_root + "cap.pcap")
post = db.mongo.construct(sample_filename, "Running", "XP-1", datetime.datetime.utcnow(), md5, 0, [""])
post_id = db.mongo.add(post)

print("\n")
for i in range(0, 31):
    misc.progress_bar.progress_bar(i, 30, "Waiting before terminating")
    sleep(1)

packet_capture.end_capture()
vm_control.end_vm(vm_path)
vm_control.restore_vm(vm_path, "Snapshot")

dns = pcap_parser.cap_dns(capture_root + "cap.pcap")
http = pcap_parser.cap_http(capture_root + "cap.pcap")

db.mongo.modify(post_id, {"$set": {"status": "Finished", "addresses": http}})
