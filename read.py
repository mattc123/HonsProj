


files = open("textout.txt", "r")
contents = files.read()
files.close()    
             
#print(contents)

word = "PCMD_MA"

if word in contents: 
   print ('Warning Drone Detected')
else:
	print("No drone detected")