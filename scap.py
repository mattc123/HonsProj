from scapy.all import sniff, wrpcap, hexdump, rdpcap
import re
import sys
#from  read import rd


#pkts_list = sniff(count = 5, monitor=False)#set monitor=True

#pkts_list.show()
#hexdump(pkts_list)
#wrpcap('scapytest.pcap',pkts_list )

#for i in pkts_list:
#	hexdump(i)

packets = rdpcap('captured.pcapng')

#print output from hexdump into txt file
sys.stdout = open('textout.txt', 'w+')

for i in packets:
	hexdump(i)	
	
#
#files = open("textout.txt", "r+")
#contents = files.read()
#files.close()   
sys.stdout.close()

#PCMD_MAG
	


	

	

