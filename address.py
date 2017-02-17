from pygeocoder import Geocoder
import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('settings.ini')
api = settings.get('SectionOne', 'geocodingapi')
import time
import re
import sys
import socks
import socket
import csv
import random

###Pulling Settings
apiquerylimit = settings.get('SectionOne', 'apiquerylimit')
useproxy = settings.get('SectionOne', 'useproxy')
useapi = settings.get('SectionOne', 'useapi')



##### Setting Variables in the Script. 
if 'true' in useapi:
	geocoder = Geocoder(api_key=api) 
else: 
	geocoder = Geocoder()
if 'true' in useproxy:
	print('boo')
#else:
#	socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="72.205.210.107", port=23952)
#	socket.socket = socks.socksocket


######## Configuring Proxy Config
#proxfile = open('proxies.cxv','rt', encoding='utf-8-sig')
#reader = csv.DictReader(proxfile)

#proxylist = []
#for row in reader:
#    proxylist.append(row)
#def getproxy():
#
#countofproxy = len(proxylist)
#randproxy = random.randint(1,countofproxy)
#currproxy = proxylist[randproxy)


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "addresses"

f = open(filename,'w')
f.close()


address_1 = input('Enter first address: ')
radius = float(input('Enter radius to check (meters, 100 min): '))

try:
    address_1_coords = geocoder.geocode(address_1).coordinates
except:
    print("API is Overlimit")
#    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="189.103.137.237", port=46423)
#    socket.socket = socks.socksocket
#    address_1_coords = geocoder.geocode(address_1).coordinates


center_lat=address_1_coords[0]
center_lon=address_1_coords[1]

start_lat=center_lat+(radius*0.001/111.3)
start_lon=center_lon-(radius*0.001/111.3)
end_lat=center_lat-(radius*0.001/111.3)
end_lon=center_lon+(radius*0.001/111.3)

sleep_cycle=0

curr_lat = start_lat
curr_lon = start_lon

while curr_lon <= end_lon:
    try:
        results = geocoder.reverse_geocode(curr_lat, curr_lon)
        if re.search("^(\d+)$",str(results[0]).split()[0]) is not None:
            l = str(results[0]).split(',')
            addr = ("%s,%s,%s"%(l[0],l[1].strip(),l[2].split()[1]))
            print (addr)
            f = open(filename,'r')
            if addr not in f.read():
                accurate_coords = geocoder.geocode(addr).coordinates
                addr = "%s,%s,%s,ROOFTOP"%(addr,accurate_coords[0], accurate_coords[1])
                f = open(filename,'a')
                f.write(addr+"\n")
            f.close()
        if curr_lat > end_lat:
            curr_lat = curr_lat - .001
        else:
            curr_lat = start_lat
            curr_lon = curr_lon + .001
        sleep_cycle = sleep_cycle + 1
        if sleep_cycle == 4:
            time.sleep(1)
            sleep_cycle = 0
    except:
        continue

