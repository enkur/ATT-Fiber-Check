from threading import Thread
from threading import RLock
from datetime import datetime

import json
import queue
import urllib.request

fileLock=RLock()
filename = 'results_'+datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
 
f = open(filename,'w')
f.write("Street, City, State, Zip, emm_lat, emm_lng, emm_acc, Speed\n")
f.close()
 
e = open('bad_addresses','w')
e.close()

state = input('Enter your State (2 letter): ')

def test(street, city, zip, emm_stuff):
    jsoncontent = {'Content-Type': 'application/json'}

    try_again = True
    while (try_again):
        try:
            url = "https://www.att.com/services/shop/model/ecom/shop/view/unified/qualification/service/CheckAvailabilityRESTService/invokeCheckAvailability"
            postdata = json.dumps({
                'userInputZip': zip,
                'userInputAddressLine1': street,
                'mode': 'fullAddress'}).encode(encoding='utf-8')
            req = urllib.request.Request(url=url, data=postdata, headers=jsoncontent, method='POST')
            resp = urllib.request.urlopen(req)
            if resp.getcode() == 200:
                speed = None
                respobj = json.loads(resp.read().decode('utf-8'))
                status = respobj['wbfcResponse']['statusName']
                if status == 'Success':
                    speed = respobj['CkavDataBean']['maxHsiaSpeedAvailable']
                    if speed is None:
                        print('No service available at %s' % street)
                    elif speed.endswith(' Mbps'):
                        speed = speed[:-5]
                else:
                    print('Availability check returned status %s' % status)

                if speed is not None:
                    line = '%s, %s, %s, %s, %s, %s, %s, %s' % \
                        (street, city, state, zip, emm_stuff[0], emm_stuff[1], emm_stuff[2], speed)
                    print(line)
                    with fileLock:
                        f = open(filename,'a')
                        f.write(line + '\n')
                        f.close()
            else:
                print('Availability check returned HTTP status %d' % resp.getcode())

            try_again=False

        except Exception as x:
            print(x)
            try_again=False
            with fileLock:
                e = open('bad_addresses','a')
                e.write(street+', '+city+', '+state+' '+emm_stuff[0]+', '+emm_stuff[1]+', '+emm_stuff[2]+', '+zip+'\n')
                e.close()
               
def run_test(i):
    i = i.strip()
    street = i.split(',')[0]
    city = i.split(',')[1]
    zip = i.split(',')[2]
    emm_stuff = i.split(',')[3:]
    test(street, city, zip, emm_stuff)

def do_stuff(q):
    while True:
        run_test(q.get())
        q.task_done()
 
q = queue.Queue(maxsize=0)
num_threads = 5
 
for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(q,))
    worker.setDaemon(True)
    worker.start()
 
houses = open('addresses','r')
 
for x in houses.readlines():
    q.put(x)

houses.close()
q.join()
