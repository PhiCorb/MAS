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

while True:
    active_post = db.mongo.find_one({"status": "Waiting"})
    if active_post is None:
        print("Found no samples queued")
        sleep(15)
    else:
        sample_id = active_post["sample_id"]
        sample_filename = active_post["filename"]
        with open(sample_root + sample_filename, "wb") as outfile:
            outfile.write(db.mongo.fs_get(sample_id).read())
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
        if active_post["machine"] == "XP-1":
            vm_path = vm_root + "XP VM 1/XP VM 1.vmx"
        else:
            print("Invalid machine in Mongo document.\nUsing XP-1.")
            vm_path = vm_root + "XP VM 1/XP VM 1.vmx"
        vm_control.spawn_vm(vm_path)
        packet_capture.start_capture("172.16.168.128", capture_root + "cap.pcap")
        db.mongo.modify(active_post["_id"], {"$set": {"status": "Running", "md5": md5, "addresses": [], "pcap": None}})

        print("\n")
        for i in range(0, int(active_post["duration"]) + 1):
            misc.progress_bar.progress_bar(i, active_post["duration"], "Waiting before terminating")
            sleep(1)

        packet_capture.end_capture()
        vm_control.end_vm(vm_path)
        vm_control.restore_vm(vm_path, "Snapshot")

        dns = pcap_parser.cap_dns(capture_root + "cap.pcap")
        http = pcap_parser.cap_http(capture_root + "cap.pcap")
        with open(capture_root + "cap.pcap", "rb") as file:
            pcap_id = db.mongo.fs_put(file)

        db.mongo.modify(active_post["_id"], {"$set": {"status": "Finished", "addresses": http, "pcap": pcap_id}})
        db.mongo.modify(active_post["_id"], {"$unset": {"sample_id": ""}})
        db.mongo.fs_delete(sample_id)
