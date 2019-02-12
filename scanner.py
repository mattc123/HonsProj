import subprocess
import platform
import re

def main(proploss):

    results = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
    results = results.decode("ascii")
    results = results.replace("\r", "")
    ls = results.split("\n")
    ls = ls[4:]# remove stuff at start of string
    
    # extract required values SSID, BSSID and RSSI
    values = ["SSID", "Signal"]# SSID returns SSID and BSSID, signal is used for RSSI
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
    print(ssid)

    values = ["MAC"]
    mac = [s for s in networks if any(xs in s for xs in values)]
    # TO DO remove label - maybe
    print(mac)

    values = ["Signal"]
    signal = [s for s in networks if any(xs in s for xs in values)]
    # print(signal) convert singal percent ro rssi values.

    # remove percent sign to the values can be manipluated
    rssi = []
    for i in signal:
        m = re.search(r"\b(\d{2})\b", i)
        if m:
            rssi.append(m.group())

    rssi = list(map(int, rssi))
    print(rssi)

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
    print(dbm)

    ## rssi to distance calculation
    distance = []
    #n = 20
    # distance = 10^((Txpower-RSSI)/10n)
    # Txpower = rssi at 1m assumed to be -54 aprox 99%
    # rssi = the recieved rssi value
    # n = signal propigation loss, higher value for indoors max 40, lower value for outside lowest 20
    for i in dbm:
        d = 10 ** ((-54 - (i)) / proploss)
        distance.append(d)

    print(['%.2f' % d for d in distance])  # 2dp for metres


#main(20)