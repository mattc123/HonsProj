#!/usr/bin/env python

#title           :finv2.py
#description     :Honours project. drone detection though SSID detection and packet analysing.
#author          :Matthew Christie
#matriculation: 1304093
#python_version  :3.7.2
#==============================================================================

#imports
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



class Interface:

	def __init__(self, master):
	#function initialising tkinter frame, widgets etc...
	

		frame = Frame(master)
		frame.grid()

		
		#creating Tkinter widgets
		#scroll textboxs
		self.tb = scrolledtext.ScrolledText(frame, width=60, height=10)
		self.tb.grid(row=0, columnspan=5)
		
		self.tb1 = scrolledtext.ScrolledText(frame, width=60, height=10)
		self.tb1.grid(row=3, columnspan=5)
		
			
		#buttons
		self.printbutton = Button(frame, text="Quit", command=frame.quit)
		self.printbutton.grid(row=1, column = 3)

		self.quitbut = Button(frame, text="Scan", command=self.scan)
		self.quitbut.grid(row=1, column=2)

		self.scanbut = Button(frame, text="Analyse", command=self.pcktscn)
		self.scanbut.grid(row=4)
		
		self.clearbut = Button(frame, text="Clear", command=self.cleartext)
		self.clearbut.grid(row=4, column=2)
		
				
		#drop down box
		var = StringVar(master)
		var.set("environment")

		self.envmenu = OptionMenu(frame, var, "Outdoors", "Indoors", "Built up area", command=self.val)
		self.envmenu.grid(row=1)

		
	def val (self, val):
	#function to assign downdown box values a numberical value 
	#so that it can be used for calculating signal loss for rssi later

		global n
		if (val == "Outdoors"):
			n = 20
		elif (val == "Indoors"):
			n = 30
		else:
			n = 40
			
	
	def cleartext(self):
	#function to clear text from all scroll text boxes
	
		self.tb.delete(1.0,END)
		self.tb1.delete(1.0,END)
	
	
	def scan (self):
	#function to find wireless networks and display them
	
		#clears the text box
		self.tb.delete(1.0,END)
		count = 1
		
		try:
			if n is None:
				print('It is None')
		except NameError:
			messagebox.showinfo("Error", "Please select an environment")
		else:
		


			#create database to store network information
			conn = sqlite3.connect('ntwks.db')
			c = conn.cursor()

			# Create table if it does not already exist
			c.execute('''CREATE TABLE IF NOT EXISTS networks
								(ssid text, bssid text, rssi real, distance real, proploss text, time text)''')

			conn.commit()
				
			#loops though 10 times to gather good sample of SSIDs
			while count < 10:
				

				# gets output from running "netsh wlan show network mode=Bssid" in command line
				# only works in windows
				results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
				#clean text 
				results = results.decode("ascii")
				results = results.replace("\r", "")
				ls = results.split("\n") 
				ls = ls[4:]
					

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
						
				#find all SSID values 
				values = ["SSID"]
				ssid = [s for s in networks if any(xs in s for xs in values)]
					
				#find all MAC values 
				values = ["MAC"]
				mac = [s for s in networks if any(xs in s for xs in values)]
					
				#find all Signal values
				values = ["Signal"]
				signal = [s for s in networks if any(xs in s for xs in values)]

				# remove special characters so the values can be manipluated
				rssi = []
				for i in signal:
					m = re.search(r"\b(\d{2})\b", i)
					if m:
						rssi.append(m.group())

				#create a list of new integers
				rssi = list(map(int, rssi))

				# convert singal percent quality to RSSI dB
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

				#rssi to distance calculation
				distance = []
				# n = 22
				# distance = 10^((Txpower-RSSI)/10n)
				# Txpower = rssi at 1m assumed to be -54 aprox 99%
				# rssi = the recieved rssi value
				# n = signal propigation loss, higher value for indoors max 44, lower value for outside lowest 20
				for i in dbm:
					d = 10 ** ((-53.6 - (i)) / n)
					distance.append(d)
					
					
					
				newdist = []
				for r in distance:
					nd = (round(r, 2))  # 2dp for metres
					newdist.append(nd)	
					
				# remove SSID: from start of list
				ssid = [s[6:] for s in ssid]
				# remove MAC: from start of list
				mac = [s[5:] for s in mac]

				#create list of tuples as it is easy to manipulate
				tup = tuple(zip(ssid, mac, rssi, newdist))

				#from 'n' value assiged in val function convert back to text
				# this is so the data is meaningful in the database
				if (n == 20):
					ploss = "Outdoors"
				elif (n == 30):
					ploss = "Indoors"
				else:
					ploss = "Built up area"

				#get the time of the current scan	
				curDT = ctime()
					
				#create a new list of tuples with signal loss and time to be stored in database
				newl = [xs + (ploss, curDT,) for xs in tup]
		

				#for every item in tuple store it in the databse
				for t in newl:
					#input mask using ? is more sucure as DB is not expecting blank values
					c.execute("INSERT OR REPLACE INTO networks VALUES (?, ?, ?, ?, ?, ?)", t)
				conn.commit()
				conn.close
					
					
				count += 1
			for newlist in tup:
					#print item in listbox
				self.tb.insert(INSERT, newlist )
				self.tb.insert(INSERT, '\n' )

			#seperate each iteration
			self.tb.insert(INSERT, '\n' )

							
				#ssid list is converted to string
			potential_drones = ''.join(ssid)
				
				#list of potential drone ssids, with wildcards as exact match is unlikly
			hazards = ["drone.*", "ar.*", "parrot.*"] 
			combined = "(" + ")|(".join(hazards) + ")"
			
				#check if wildcards appear in ssid list
			matched = re.match(combined, potential_drones)
				
			if matched:
					#convert to string
				match = str(matched)
					#remove irrelevent data at start and end of string
				match = match[32:-1]
					
					#print in scroll box to user
				self.tb1.insert(INSERT, match)
				self.tb1.insert(INSERT, '\n' )
					
				#display an alert
				messagebox.showwarning("Warning", "Potential Drone Presence Detected")
			else:
				messagebox.showinfo("Warning", "No Drones Detected")
				
				
			
	def pcktscn(self):
	#function to capture communication packets between drone and pilot and analyise them

		#sniff incoming packets
		pkts_list = sniff(count=50, monitor=False)  # set monitor=True #count  > 50 for greater sample

		#save as pcap for future analysis
		wrpcap('scapytest.pcap', pkts_list)
		
		
		#store state of sys.stdout for later
		orig_stdout = sys.stdout
		
		#write input to text file
		sys.stdout = open('textout.txt', 'w+')
		for i in pkts_list:
			hexdump(i)
		sys.stdout.close()
		
		#revert to original state for sys.stdout. This stops output from being written into the text file and instead back into the console
		sys.stdout = orig_stdout
	

		#read from the file just created and written to
		files = open("textout.txt", "r")
		contents = files.read()
		files.close()

		#list of identifying drone features in packets. PCMD_MA = parrot drones
		#more can be added here in the future for more comprehensive detection
		drones = ["PCMD_MA", "Drone model2", "Drone model3"]

		#if any features appear in the capture packets disaply a drone has been detected to the user
		if any(x in contents for x in drones):
			
			self.tb1.insert(END, 'Drone Detected' )
			self.tb1.insert(END, '\n' )
			messagebox.showwarning("Warning", "Drone Presence Confirmed")
			
			# if no match is found display no presence is detected to the user.
		else:
			self.tb1.insert(END, "No Drone Detected" )
			self.tb1.insert(END, '\n' )
			messagebox.showinfo("Warning", "No Drones Detected")


#tkinter frame set up
root = Tk()
root.title("Drone Detection")
root.geometry("650x500")

b = Interface(root)

root.mainloop()