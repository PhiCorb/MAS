import pyshark
import colorama

colorama.init()
# cap_file = "/home/phil/Desktop/test1.pcap"


def cap_http(pcap_file):
    cap = pyshark.FileCapture(pcap_file, display_filter="http")
    hosts = []

    for x in cap:
        if x["ip"].src == "172.16.168.128":
            if x["http"].host not in hosts:
                hosts.append(x["http"].host)

    print("The following hosts were contacted (HTTP):")
    for i in hosts:
        print("\t" + i)


def cap_dns(pcap_file):
    cap = pyshark.FileCapture(pcap_file, display_filter="dns")
    dns = []

    for x in cap:
        if x["ip"].src == "172.16.168.128":
            if x["dns"].qry_name not in dns:
                dns.append(x["dns"].qry_name)
    print("The following DNS resolutions were requested:")
    for i in dns:
        print("\t" + i)


if __name__ == "__main__":
    print(colorama.Fore.WHITE + colorama.Back.RED + "ERROR: this is not intended to be executed directly!" +
          colorama.Style.RESET_ALL)
    exit(1)