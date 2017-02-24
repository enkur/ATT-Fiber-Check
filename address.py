from pygeocoder import Geocoder,GeocoderError
import time
import re
import sys
import random
import os.path
import argparse
import configparser

# Read in settings from settings.ini file
settings = configparser.ConfigParser()
settings.read('settings.ini')

# The Args the Args Thank God for the args (CronJob Ho!)
parser = argparse.ArgumentParser()
parser.add_argument("--resume","-r",help="Resume Existing job and filling in API.  -r 500 (api limit 500)")
args = parser.parse_args()
if args.resume:
    shouldcontinue = 'y'
    apiquerylimit = args.resume

# Setup Geocoder using the API key if this has been enabled in settings.  If not, assume no API key
geocoderApiKey=None
if 'true' in settings.get('Address', 'useapi'):
    geocoderApiKey = settings.get('Address', 'geocodingapi')
    print ('Using API Key')
geocoder = Geocoder(api_key=geocoderApiKey)


#File Names and Array setup
workdone = "workdone"
test = "test"
filename = "addresses"
toberemoved = []
latlong = []
completed = []


#This function removes duplicates from any array that comes into it.  Handy to reduce API Query 
def remove_duplicates(list):
    newlist = []
    for i in list:
        if i not in newlist:
            newlist.append(i)
    return newlist

#Meat and potatos, This function generates all the coords.  It's a one stop shop. Give it a starting address, and a radius and returns an array size of your choosing
def generate_coords(faddress, sradius):

    try:
        address_1_coords = geocoder.geocode(faddress).coordinates
    except GeocoderError as e:
        print('Geocoder: '+ e.args)
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
            print('Geocoder: '+ e.args)
            input("Press Enter to exit...")
    thelist = remove_duplicates(thelist)
    return thelist

#This tests the Google geocoding API, returns an address based off of Lat/Lon.  It then geocodes the address again to have a "more accurate" set of coords.  This is 2 hits per VALID address.  
def test_address(curr_lat, curr_lon):
    try:
        #Below returns an Address when like '5555 Some Street, Some Town, MO 55511, USA' when called by arg[0] aka str(result[0])
        results = geocoder.reverse_geocode(float(curr_lat), float(curr_lon))
      
        #Below this is a REGEX Search basically it splits off the first part of the address and checks if there is a number only.  If assigning this to a variable, the value = <_sre.SRE_Match object; span=(0, 5), match='5555'>
        if re.search("^(\d+)$",str(results[0]).split()[0]) is not None:
           
           
           
            ##
            #l = '5555 Some Street, Some Town, MO 55511, USA'
            #l[0] = '5555 Some Street'
            #l[1] = 'Some Town'
            #l[2] = 'MO 55511'
            l = str(results[0]).split(',') 



            # addr basically reforms the line without the state '5555 Some Street, Some Town,55511'
            addr = ("%s,%s,%s"%(l[0],l[1].strip(),l[2].split()[1]))

            ###Recheckign the coords for the address.
            accurate_coords = geocoder.geocode(addr).coordinates

            #Basically adds the new cords to the existing, Ala 5555 Some Street, Some Town,55511,ROOFTOP,38.4444,-102
            addr = "%s,%s,%s,ROOFTOP"%(addr,accurate_coords[0], accurate_coords[1])
            print (addr)
            return addr
    except GeocoderError as e:
        print("error: ", e.args)
        return e.args
    except IndexError:
        #Probably missing zip code
        return None

    
###IF we don't do this we get duplicates in the list and that just causes more API Hits. 
def remove_duplicates(list):
    newlist = []
    for i in list:
        if i not in newlist:
            newlist.append(i)
    return newlist


###
### Begin Main Program Logic Here
###


###Add a Resume Function here
try:
    shouldcontinue
except:
    shouldcontinue = input('Should we continue an existing job?(y or yes)')

if 'y' in shouldcontinue:
    #Adding better smarts for Args
    if os.path.exists(workdone) and os.path.getsize(workdone) > 0:
        print("File Exists")
        curworking = open('workdone','r')
        for g in curworking.readlines():
            g = g.strip('\n')
            g = g.strip()
            g = g.replace(" ", "")
            
            latlong.append(g.split(','))

    else:
        #print("file Doesn't Exist")
        #file2 = open(workdone,'w')
        #file2.close()
        ###IF the file doesn't exist, it shouldn't go on. 
        print("Exiting NO files to workwith or no data Cannot Resume")
        sys.exit()
        #f = open(filename,'w')
        #f.close()
else:
    iaddress = input('Enter first address: ')
    iradius = float(input('Enter radius to check (meters, 100 min): '))
    latlong = generate_coords(iaddress, iradius) 

try:
    apiquerylimit
except NameError:
    apiquerylimit = int(input('Api limit (Recommend 1000): '))














####MAIN BODY

#adding a catch for less matches then query limit
if len(latlong) < apiquerylimit:
    apiquerylimit = len(latlong)
sleep_cycle = 0
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
