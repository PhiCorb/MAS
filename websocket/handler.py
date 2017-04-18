from sys import stdout
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import datetime
import base64
import json

# # Count from 1 to 10 with a sleep
# for count in range(0, 10):
#     print(count + 1)
#     stdout.flush()
#     sleep(0.5)

client = MongoClient("localhost", 27017)
db = client.mas
collection = db.jobs

fs_db = client.mas_samples
fs = gridfs.GridFS(fs_db)

b64file = ""

while True:
    command = input()

    if command == "home":
        analysed = collection.find({"status": "Finished"}).count()
        processing = collection.find({"status": "Running"}).count()
        waiting = collection.find({"status": "Waiting"}).count()
        print("{} {} {}".format(analysed, processing, waiting))
        stdout.flush()
    elif command == "active":
        active_cursor = collection.find({"status": "Running"}, {"filename": 1, "machine": 1, "date_time": 1})
        active_list = []
        for post in active_cursor:
            active_list.append(post)
        for post in active_list:
            post.update({"_id": str(post["_id"])})
            post.update({"date_time": post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_list))
        stdout.flush()
    elif command == "waiting":
        active_cursor = collection.find({"status": "Waiting"}, {"filename": 1, "machine": 1, "date_time": 1})
        active_list = []
        for post in active_cursor:
            active_list.append(post)
        for post in active_list:
            post.update({"_id": str(post["_id"])})
            post.update({"date_time": post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_list))
        stdout.flush()
    elif command == "jobs":
        active_cursor = collection.find({}, {"filename": 1, "machine": 1, "date_time": 1})
        active_list = []
        for post in active_cursor:
            active_list.append(post)
        for post in active_list:
            post.update({"_id": str(post["_id"])})
            post.update({"date_time": post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_list))
        stdout.flush()
    elif command == "details":
        target_id = input()
        active_post = collection.find_one({"_id": ObjectId(target_id)}, {"pcap": 0, "sample_id": 0})
        # if active_post["status"] == "Waiting":
        #     print("WAITING")
        # elif active_post["status"] == "Running":
        #     print("RUNNING")
        # else:
        active_post.update({"_id": str(active_post["_id"])})
        active_post.update({"date_time": active_post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_post))
        stdout.flush()
    elif command == "upload":
        analysed = collection.find({"status": "Finished"}).count()
        processing = collection.find({"status": "Running"}).count()
        waiting = collection.find({"status": "Waiting"}).count()
        response = "{} {} {}".format(analysed, processing, waiting)
        vms = ["XP-1"]  # TODO: read in from JSON
        for vm in vms:
            response += " {}".format(vm)
        print(response)
        stdout.flush()
    elif command == "file":
        # with open("/home/phil/Desktop/test.log", "a") as file:
        #     file.write(command)
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

        # with open("/home/phil/Desktop/out.exe", "wb") as file:
        #     out = base64.b64decode(b64file)
        #     if out[0] == 0x7e and out[1] == 0x29 and out[2] == 0x5e:
        #         out = out[3:]
        #     else:
        #         print("Hex bug not matched. [0] = {}, [1] = {}, [2] = {}".format(out[0], out[1], out[2]))
        #     file.write(out)
        #     grid_file = fs.put(out)

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
        # with open("/home/phil/Desktop/test_decode.log", "wb") as file:
        #     file.write(base64.b64decode(b64file))
    else:
        with open("/home/phil/Desktop/test.log", "a") as file:
            file.write(command)
        command = command.split(",", 1)
        if len(command) == 2:
            b64file += command[1]
        else:
            b64file += command[0]

