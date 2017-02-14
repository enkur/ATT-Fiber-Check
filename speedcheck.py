from threading import Thread
from splinter import Browser
from datetime import datetime

import re
import sys
import time
import queue

filename = 'results_'+datetime.now().strftime("%Y-%m-%d")
 
f = open(filename,'w')
f.write("Street, City, State, Zip, emm_lat, emm_lng, emm_acc, Speed\n")
f.close()
 
e = open('bad_addresses','w')
e.close()

state = input('Enter your State (2 letter): ')

def test(street, city, zip, emm_stuff):
        try_again = True
        while (try_again):
                try:
                    f = open(filename,'a')
                    browser = Browser('phantomjs')
                    url = "https://www.att.com/shop/unified/availability.html"
                    browser.visit(url)
                    browser.find_by_id('streetaddress').fill(street)
                    browser.find_by_id('zipcode').fill(zip)
                    browser.find_by_xpath('//*[@id="content"]/div/div[2]/div[1]/div/div/div/form/div[2]/input').first.click()
                    if browser.is_text_present('your home qualifies for AT&T Fiber', wait_time=10):
                        speed = '1000'
                    elif browser.is_text_present('You can get AT&T Fiber at your home', wait_time=10):
                        speed = '1000'
                    elif browser.is_text_present('Mbps', wait_time=10):
                        if browser.is_text_present('Select the services you’re interested in'):
                                element = browser.find_by_xpath('//*[@id="offerTilesDiv"]/div[1]/div[1]/div/div[5]/div[2]/div[2]/p[1]/span[2]')
                                speed = re.search("(\d+)",element.text).group(0)
                        else:
                                element = browser.find_by_xpath('//*[@id="content"]/div/div[1]/div[5]/div[1]/div/div[2]/div[2]/div/span/div/div[2]/p[1]/span')
                                speed = re.search("(\d+)",element.text).group(0)
                    else:
                        speed = '0'
                    if speed == '0':
                            print ('bad address')
                    else:
                            print (street+', '+city+', '+state+', '+zip+', '+emm_stuff[0]+', '+emm_stuff[1]+', '+emm_stuff[2]+', '+speed)
                            f.write(street+', '+city+', '+state+', '+zip+', '+emm_stuff[0]+', '+emm_stuff[1]+', '+emm_stuff[2]+', '+speed+'\n')
                    browser.quit()
                    try_again=False
                    f.close()
                except:
                    try_again=False
                    e = open('bad_addresses','a')
                    e.write(street+', '+city+', '+state+' '+emm_stuff[0]+', '+emm_stuff[1]+', '+emm_stuff[2]+', '+zip+'\n')
                    e.close()
                    browser.quit()
               
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

q.join()
