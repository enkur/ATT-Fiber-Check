from pygeocoder import Geocoder,GeocoderError
import time
import re
import sys
import random
import os.path

#File Names
geocoder = Geocoder()
workdone = "workdone"
test = "test"
filename = "addresses"
toberemoved = []


###Old write File
#f = open(filename,'w')
#f.close()
#f = open(filename,'w')
#f.close()
latlong = []
completed = []

geocoder = Geocoder()


sleep_cycle=0

def remove_duplicates(list):
    newlist = []
    for i in list:
        if i not in newlist:
            newlist.append(i)
    return newlist

def generate_coords(faddress, sradius):

    try:
        address_1_coords = geocoder.geocode(faddress).coordinates
    except GeocoderError as e:
        print('Geocoder: '+str(e))
        input("Press Enter to exit...")
        sys.exit()

    center_lat=address_1_coords[0]
    center_lon=address_1_coords[1]
    #center_lat=38.559086
    #center_lon=-90.40435699999999
    
    start_lat=center_lat+(sradius*0.001/111.3)
    start_lon=center_lon-(sradius*0.001/111.3)
    end_lat=center_lat-(sradius*0.001/111.3)
    end_lon=center_lon+(sradius*0.001/111.3)
    
    sleep_cycle=0
    
    curr_lat = start_lat
    curr_lon = start_lon

    thelist = []
    while curr_lon <= end_lon:
        try:
            thelist.append([curr_lat, curr_lon])
    
            if curr_lat > end_lat:
                curr_lat = curr_lat - .001
            else:
                curr_lat = start_lat
                curr_lon = curr_lon + .001
        except GeocoderError as e:
            print('Geocoder: '+str(e))
            input("Press Enter to exit...")
            sys.exit()
    thelist = remove_duplicates(thelist)
    return thelist


def test_address(curr_lat, curr_lon):
    try:
        results = geocoder.reverse_geocode(float(curr_lat), float(curr_lon))
        if re.search("^(\d+)$",str(results[0]).split()[0]) is not None:
            l = str(results[0]).split(',')
            addr = ("%s,%s,%s"%(l[0],l[1].strip(),l[2].split()[1]))
            accurate_coords = geocoder.geocode(addr).coordinates
            addr = "%s,%s,%s,ROOFTOP"%(addr,accurate_coords[0], accurate_coords[1])
            print (addr)
            return addr
    except GeocoderError:
        print("error: ", GeocoderError.G_GEO_OVER_QUERY_LIMIT)
        return GeocoderError.G_GEO_OVER_QUERY_LIMIT
    


    
###IF we don't do this we get duplicates in the list and that just causes more API Hits. 
def remove_duplicates(list):
    newlist = []
    for i in list:
        if i not in newlist:
            newlist.append(i)
    return newlist

###Add a Resume Function here
shouldcontinue = input('Should we continue an existing job?(y or yes)')

if 'y' in shouldcontinue:
    if os.path.exists(workdone) == True:
        print("File Exists")
        curworking = open('workdone','r')
        for g in curworking.readlines():
            g = g.strip('\n')
            g = g.strip()
            
            latlong.append(g.split(','))

    else:
        print("file Doesn't Exist")
        #file2 = open(workdone,'w')
        #file2.close()
        f = open(filename,'w')
        f.close()
else:
    iaddress = input('Enter first address: ')
    iradius = float(input('Enter radius to check (meters, 100 min): '))
    latlong = generate_coords(iaddress, iradius) 

apiquerylimit = int(input('Api limit (Recommend 1000): '))
#print(latlong)













####MAIN BODY

#adding a catch for less matches then query limit
if len(latlong) < apiquerylimit:
    apiquerylimit = len(latlong)

count = 0
while count < apiquerylimit:
    curraddr = test_address(latlong[count][0],latlong[count][1])
    if curraddr is not None:
        if 'OVER_QUERY_LIMIT' in curraddr:
            print("OVER LIMIT API, EXITING AND WRITING RESULTS")
            break
        else:
            toberemoved.append(latlong[count])
            completed.append(curraddr)
    elif curraddr is None:
        toberemoved.append(latlong[count])
    sleep_cycle = sleep_cycle + 1
    if sleep_cycle == 4:
        time.sleep(1)
        sleep_cycle = 0
    count = count + 1
    print(count)

####Removes Items We Already Did
for t in toberemoved:
    latlong.remove(t)

#### writes the remaining items to file (to be worked on later

remakefile = open('workdone','w')
remakefile.close()
for t in latlong:
    curwork = "%s, %s"%(t[0], t[1])
    f = open(workdone,'a')
    f.write(curwork+"\n")

completed = remove_duplicates(completed)

#### writes the new completed addresses.
for t in completed:
    addressoutput = "%s"%(t)
    #f = open(test,'a')
    f = open(filename,'a')
    f.write(addressoutput+"\n")
