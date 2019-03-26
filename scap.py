from scapy.all import sniff, wrpcap, hexdump, rdpcap
import re
import sys

#################################packet capture ############################


pkts_list = sniff(count = 10, monitor=False)#set monitor=True #count = > 10 for greater sample

wrpcap('scapytest.pcap',pkts_list )

sys.stdout = open('textout.txt', 'w+')
for i in pkts_list:
	hexdump(i)
sys.stdout.close()

######################################packets on saved scan###################

#packets = rdpcap('captured.pcapng')

#print output from hexdump into txt file
#sys.stdout = open('textout.txt', 'w+')

#for i in packets:
#	hexdump(i)	
	
#
#files = open("textout.txt", "r+")
#contents = files.read()
#files.close()   
#sys.stdout.close()

#PCMD_MAG
	


	

	

