# ATT-Fiber-Check
program to check where Fiber is available

Credit to MTdoyle for the original Century Link  speed checker
https://github.com/mtdoyle/cl_speedcheck

Requires Python 3.6  (3.5 May WORK)
(tested on FRESH install of ubuntu 16.04 Installed PYTHON3.5, Pip3 and below)

  
  ```bash
  sudo apt install python3.5
  Sudo apt install python3-pip
  pip3 install splinter
  pip3 install pygeocoder  #(MAY NEED to use sudo -H pip3 install pygeocoder)
  ```
  
If running 
splinter package (pip install splinter)  
phantomjs web driver  




ON UBUNTU 16.04 A Script was Found [here](https://gist.github.com/julionc/7476620)
pygeocoder package (pip install pygeocoder)


run address.py and give it a starting address and a radius in meters to search within.  
Starting Address in Quotes "1600 Pennsylvania Ave NW, Washington, DC 20006"

These results are written to a file 
give a minimum of 100 meters. 1600 meters(1 mile) resulted in 400 addresses so be careful.

run speedcheck.py to query the addresses with AT&T and will report back if Fiber is available and if not then what other speeds are offered.

use http://www.easymapmaker.com to create the map from the results file

The code probably needs lots of clean up. I have never programmed in Python until yesterday so forgive me for inaccuracies.
I am just glad I was able to port this over from the Century Link folks on dslr.

Anyone is welcome to modify and improve the code.
