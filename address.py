from pygeocoder import Geocoder
import time
import re
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "addresses"

f = open(filename,'w')
f.close()

geocoder = Geocoder()

address_1 = input('Enter first address: ')
radius = float(input('Enter radius to check (meters, 100 min): '))

address_1_coords = geocoder.geocode(address_1).coordinates

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
