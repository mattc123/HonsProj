from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import subprocess
import platform #finding OS
import re
import sqlite3
from time import ctime
from scapy.all import sniff, wrpcap, hexdump, rdpcap
import re
import sys


class Butts:

	def __init__(self, master):
	

		frame = Frame(master)
		frame.grid()

		# self.tb = Text(frame)
		self.tb = scrolledtext.ScrolledText(frame, width=60, height=10)
		self.tb.grid(row=0, columnspan=5)
		
		self.tb1 = scrolledtext.ScrolledText(frame, width=60, height=10)
		self.tb1.grid(row=3, columnspan=5)
		
			
		self.printbutton = Button(frame, text="Quit", command=frame.quit)
		self.printbutton.grid(row=1, column = 3)

		self.quitbut = Button(frame, text="Scan", command=self.scan)
		self.quitbut.grid(row=1, column=2)

		self.scanbut = Button(frame, text="Detect", command=self.pcktscn)
		self.scanbut.grid(row=4)
		
		
		self.clearbut = Button(frame, text="Clear", command=self.cleartext)
		self.clearbut.grid(row=4, column=2)
		
		
		

		var = StringVar(master)
		var.set("environment")

		self.envmenu = OptionMenu(frame, var, "Outdoors", "Indoors", "Built up area", command=self.val)
		self.envmenu.grid(row=1)

	def val (self, val):

		global n #temporary solution
		if (val == "Outdoors"):
			n = 20
		elif (val == "Indoors"):
			n = 30
		else:
			n = 40
			
	
	def cleartext(self):
		self.tb.delete(1.0,END)
		self.tb1.delete(1.0,END)
	
	
	def scan (self):

		count = 1
		while count < 10:
	
			try:
				if n is None:
					print('It is None')
			except NameError:
				messagebox.showinfo("Error", "Please select an environment")
			else:

				conn = sqlite3.connect('ntwks.db')
				c = conn.cursor()

				# Create table if it does not already exist
				c.execute('''CREATE TABLE IF NOT EXISTS networks
									(ssid text, bssid text, rssi real, distance real, proploss text, time text)''')

				conn.commit()

				results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
				results = results.decode("ascii")
				results = results.replace("\r", "")
				ls = results.split("\n")
				ls = ls[4:]
				# remove stuff at start of string

				# extract required values SSID, BSSID and RSSI
				values = ["SSID", "Signal"]
				new = [s for s in ls if any(xs in s for xs in values)]

				# replace BSSID with MAC
				new = [w.replace('BSSID', 'MAC') for w in new]

				# remove extra whitespace
				networks = []
				for i in new:
					j = i.replace(' ', '')
					networks.append(j)
				# print(networks)	

				values = ["SSID"]
				ssid = [s for s in networks if any(xs in s for xs in values)]
				# TO DO remove ssid label - maybe

				values = ["MAC"]
				mac = [s for s in networks if any(xs in s for xs in values)]
				# TO DO remove label - maybe

				values = ["Signal"]
				signal = [s for s in networks if any(xs in s for xs in values)]
				# print(signal) convert signal percent ro rssi values.

				# remove percent sign to the values can be manipluated
				rssi = []
				for i in signal:
					m = re.search(r"\b(\d{2})\b", i)
					if m:
						rssi.append(m.group())

				rssi = list(map(int, rssi))

				# convert singal percent quality to RSSI dBm
				# -50 = strongest signal,  -100 = weakest
				dbm = []
				for i in rssi:
					if i <= 0:
						val = -100
					elif i >= 100:
						val = -50
					else:
						val = (i / 2) - 100
						dbm.append(val)  # list of rssi dBm values

				# ## rssi to distance calculation
				distance = []
				# n = 22
				# distance = 10^((Txpower-RSSI)/10n)
				# Txpower = rssi at 1m assumed to be -54 aprox 99%
				# rssi = the recieved rssi value
				# n = signal propigation loss, higher value for indoors max 44, lower value for outside lowest 20
				for i in dbm:
					d = 10 ** ((-54 - (i)) / n)
					distance.append(d)

				ssid = [s[6:] for s in ssid]  # remove SSID: from start of list
				mac = [s[5:] for s in mac]  # remove MAC: from start of list

				tup = tuple(zip(ssid, mac, rssi, distance))
				# print(tup)

				if (n == 20):
					ploss = "Outdoors"
				elif (n == 30):
					ploss = "Indoors"
				else:
					ploss = "Built up area"

				curDT = ctime()
				newl = [xs + (ploss, curDT,) for xs in tup]
				print(newl)

				for t in newl:
					c.execute("INSERT OR REPLACE INTO networks VALUES (?, ?, ?, ?, ?, ?)", t)
				conn.commit()
				conn.close
				

				
				############################################
				
					
			#print item	in listbox
			for newlist in tup:
				self.tb.insert(INSERT, newlist )
				self.tb.insert(INSERT, '\n' )
			
			count += 1
			
						
		potential_drones = ''.join(ssid)
			
			
		hazards = ["BT.*","drone.*", "ar.*", "parrot.*"]
		combined = "(" + ")|(".join(hazards) + ")"
		
		matched = re.match(combined, potential_drones)
		if matched:
			print(matched)
			match = str(matched)
			match = match[32:-1]
			
			
			self.tb1.insert(INSERT, match)
			self.tb1.insert(INSERT, '\n' )
			messagebox.showwarning("Warning", "Potential Drone Presence Detected")
				
			
			
			
			#regex = re.compile('BT*')
						
			#matches = [string for string in ssid if re.match(regex, string)]
			
			#print (matches)


	def pcktscn(self):
		#################################packet capture ############################
		pkts_list = sniff(count=10, monitor=False)  # set monitor=True #count = > 10 for greater sample

		wrpcap('scapytest.pcap', pkts_list)

		orig_stdout = sys.stdout
		
		sys.stdout = open('textout.txt', 'w+')
		for i in pkts_list:
			hexdump(i)
		sys.stdout.close()
		
		#print back out to console
		sys.stdout = orig_stdout
	

		files = open("textout.txt", "r")
		contents = files.read()
		files.close()

		drones = ["PCMD_MA", "Drone model2", "Drone model3"]

		if any(x in contents for x in drones):
			
			self.tb1.insert(END, 'hello world' )
			self.tb1.insert(END, '\n' )
			messagebox.showwarning("Warning", "Drone Presence Confirmed")
		else:
			
			self.tb1.insert(END, "No Drone Detected" )
			self.tb1.insert(END, '\n' )
			messagebox.showinfo("Warning", "No Drones Detected")


root = Tk()
root.title("Drone Detection")
root.geometry("650x500")



b = Butts(root)

root.mainloop()