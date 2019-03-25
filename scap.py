from scapy.all import sniff, wrpcap, hexdump, rdpcap


#pkts_list = sniff(count = 5, monitor=False)#set monitor=True

#pkts_list.show()
#hexdump(pkts_list)
#wrpcap('scapytest.pcap',pkts_list )

#for i in pkts_list:
#	hexdump(i)



packets = rdpcap('test1.pcapng')

for i in packets:
	hexdump(i)
	
	

	
	
	
