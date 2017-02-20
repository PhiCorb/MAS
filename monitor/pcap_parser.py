import pyshark

cap = pyshark.FileCapture('/home/phil/Desktop/test1.cap', display_filter="http")
hosts = []

for x in cap:
    if x["ip"].src == "172.16.168.128":
        if x["http"].host not in hosts:
            hosts.append(x["http"].host)

print("The following hosts were contacted:")
for i in hosts:
    print("\t" + i)
