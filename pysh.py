import pyshark

cap = pyshark.LiveCapture(output_file="test.pcap")
cap.sniff(timeout=20)
cap


