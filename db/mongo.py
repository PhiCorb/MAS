from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import colorama
from datadog import statsd

colorama.init()

client = MongoClient("localhost", 27017)
db = client.mas
collection = db.jobs

fs_db = client.mas_samples
fs = gridfs.GridFS(fs_db)


def construct(filename, status, machine, date_time, md5, duration, addresses, pcap=None):
    post = {"filename": filename,
            "status": status,
            "machine": machine,
            "date_time": date_time,
            "md5": md5,
            "duration": duration,
            "addresses": addresses,
            "pcap": pcap}
    return post


def add(post):
    post_id = collection.insert_one(post).inserted_id
    statsd.increment('mongo.requests', 1)
    return post_id


def find_one(bson):
    post = collection.find_one(bson)
    statsd.increment('mongo.requests', 1)
    return post


def fs_put(file):
    statsd.increment('mongo.requests', 1)
    return fs.put(file)


def fs_get(obj_id):
    statsd.increment('mongo.requests', 1)
    return fs.get(obj_id)


def fs_delete(obj_id):
    statsd.increment('mongo.requests', 1)
    return fs.delete(obj_id)


def modify(post_id, updated_bson):
    result = collection.update_one({"_id": ObjectId(post_id)}, updated_bson)
    statsd.increment('mongo.requests', 1)
    if result.matched_count == 1 and result.modified_count == 1:
        return 1
    else:
        return 0


def delete(post_id):
    result = collection.delete_one({"_id": ObjectId(post_id)})
    statsd.increment('mongo.requests', 1)
    if result.deleted_count == 1:
        return 1
    else:
        return 0

if __name__ == "__main__":
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: this is not intended to be executed directly!" +
          colorama.Style.RESET_ALL)
    exit(1)
