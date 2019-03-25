from scapy.all import sniff, wrpcap, hexdump


pkts_list = sniff(count=1, monitor=False)#set monitor=True

pkts_list.show()



#hexdump(pkts_list)



#wrpcap('scapytest.pcap',pkts_list )
hexdump(pkts_list[0])