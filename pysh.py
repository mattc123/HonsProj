import pyshark

cap = pyshark.LiveCapture(interface='Wi-Fi 2', output_file="test.pcap")
cap.sniff(timeout=20)
cap

#https://www.adminsub.net/mac-address-finder/Parrot

