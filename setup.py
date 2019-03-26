import sqlite3

#########################basic sqlite setup#######################
conn = sqlite3.connect('ntwks.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS networks
				(ssid text, bssid text, rssi text, distance real)''')

# Insert a row of data
#c.execute("INSERT INTO networks VALUES ('mywifi12','mac123','55p',4)")


c.execute ("SELECT * FROM networks WHERE ssid = 'mywifi12'")
print (c.fetchall())


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()