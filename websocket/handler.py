from sys import stdout
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import datetime
import base64
import os
import json
from datadog import statsd

client = MongoClient("localhost", 27017)
db = client.mas
collection = db.jobs

fs_db = client.mas_samples
fs = gridfs.GridFS(fs_db)

b64file = ""
base_path = os.path.dirname(os.path.realpath(__file__))
json_name = "/config.json"

try:
    with open(base_path + json_name) as json_file:
        config = json.load(json_file)
    username = config["username"]
    password = config["password"]
except FileNotFoundError:
    username = "undefined"
    password = "undefined"


while True:
    # Get client data
    command = input()

    if command == "auth":
        user_in = input()
        pass_in = input()
        if user_in == username:
            if pass_in != password:
                print("bad")
                stdout.flush()
                exit(1)
        else:
            print("bad")
            stdout.flush()
            exit(1)
        print("ok")
        stdout.flush()
    if command == "home":
        analysed = collection.find({"status": "Finished"}).count()
        processing = collection.find({"status": "Running"}).count()
        waiting = collection.find({"status": "Waiting"}).count()
        statsd.increment('mongo.requests', 3)
        print("{} {} {}".format(analysed, processing, waiting))
        statsd.increment('server.commands', 1)
        stdout.flush()
    elif command == "active":
        active_cursor = collection.find({"status": "Running"}, {"filename": 1, "machine": 1, "date_time": 1})
        statsd.increment('mongo.requests', 1)
        active_list = []
        for post in active_cursor:
            active_list.append(post)
        for post in active_list:
            post.update({"_id": str(post["_id"])})
            post.update({"date_time": post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_list))
        statsd.increment('server.commands', 1)
        stdout.flush()
    elif command == "waiting":
        active_cursor = collection.find({"status": "Waiting"}, {"filename": 1, "machine": 1, "date_time": 1})
        statsd.increment('mongo.requests', 1)
        active_list = []
        for post in active_cursor:
            active_list.append(post)
        for post in active_list:
            post.update({"_id": str(post["_id"])})
            post.update({"date_time": post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_list))
        statsd.increment('server.commands', 1)
        stdout.flush()
    elif command == "jobs":
        active_cursor = collection.find({}, {"filename": 1, "machine": 1, "date_time": 1})
        statsd.increment('mongo.requests', 1)
        active_list = []
        for post in active_cursor:
            active_list.append(post)
        for post in active_list:
            post.update({"_id": str(post["_id"])})
            post.update({"date_time": post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_list))
        statsd.increment('server.commands', 1)
        stdout.flush()
    elif command == "details":
        target_id = input()
        active_post = collection.find_one({"_id": ObjectId(target_id)}, {"pcap": 0, "sample_id": 0})
        statsd.increment('mongo.requests', 1)
        active_post.update({"_id": str(active_post["_id"])})
        active_post.update({"date_time": active_post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_post))
        statsd.increment('samples.viewed', 1)
        statsd.increment('server.commands', 1)
        stdout.flush()
    elif command == "upload":
        analysed = collection.find({"status": "Finished"}).count()
        processing = collection.find({"status": "Running"}).count()
        waiting = collection.find({"status": "Waiting"}).count()
        statsd.increment('mongo.requests', 3)
        response = "{} {} {}".format(analysed, processing, waiting)
        vms = ["XP-1"]  # Change this if adding additional VMs
        for vm in vms:
            response += " {}".format(vm)
        print(response)
        statsd.increment('server.commands', 1)
        stdout.flush()
    elif command == "file":
        sample_filename = input()
        sample_machine = input()
        sample_duration = input()
        while command != "file_done":
            command = command.split(",", 1)
            if len(command) == 2:
                b64file += command[1]
            else:
                b64file += command[0]
            command = input()

        out = base64.b64decode(b64file)
        if out[0] == 0x7e and out[1] == 0x29 and out[2] == 0x5e:
            out = out[3:]
        grid_file = fs.put(out)
        post = {
            "filename": sample_filename,
            "machine": sample_machine,
            "duration": sample_duration,
            "date_time": datetime.datetime.utcnow(),
            "status": "Waiting",
            "sample_id": grid_file
        }
        post_id = collection.insert_one(post).inserted_id
        statsd.increment('mongo.requests', 2)
        statsd.increment('samples.added', 1)
        statsd.increment('server.commands', 1)
    elif command == "pcap":
        target_id = input()
        active_post = collection.find_one({"_id": ObjectId(target_id)}, {"pcap": 1})
        pcap = fs.get(active_post["pcap"])
        statsd.increment('mongo.requests', 2)
        b64file = base64.b64encode(pcap.read()).decode("ascii")
        chunk_size = 130000
        for i in range(0, len(b64file), chunk_size):
            print(b64file[i:i+chunk_size])
            stdout.flush()
        print("finished.")
        statsd.increment('server.commands', 1)
        stdout.flush()
    # ---Debug code---
    # else:
    #     with open("/home/phil/Desktop/test.log", "a") as file:
    #         file.write(command)
    #     command = command.split(",", 1)
    #     if len(command) == 2:
    #         b64file += command[1]
    #     else:
    #         b64file += command[0]

