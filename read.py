files = open("textout.txt", "r")
contents = files.read()
files.close()    
             
drones = ["PCMD_MA", "Drone model2", "Drone model3"]



if any(x in contents for x in drones):
   print ('Warning Drone Detected')
else:
	print("No drone detected")