from sys import stdout
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import json

# # Count from 1 to 10 with a sleep
# for count in range(0, 10):
#     print(count + 1)
#     stdout.flush()
#     sleep(0.5)

client = MongoClient("localhost", 27017)
db = client.mas
collection = db.jobs

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
        active_post = collection.find_one({"_id": ObjectId(target_id)})
        active_post.update({"_id": str(active_post["_id"])})
        active_post.update({"date_time": active_post["date_time"].strftime("%Y-%m-%d %H:%M:%S")})
        print(json.dumps(active_post))
        stdout.flush()
