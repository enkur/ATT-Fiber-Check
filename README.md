# ATT-Fiber-Check
program to check where Fiber is available

Credit to MTdoyle for the original Century Link  speed checker
https://github.com/mtdoyle/cl_speedcheck

Requires Python 3.6  (3.5 May WORK)  
requires splinter package (pip install splinter or pip3 install splinter)  
requires pygeocoder package (pip install splinter or pip3 install splinter)  
Requires Phantomjs Web driver [Original Makers](http://phantomjs.org/)  
  
  

Ubuntu 16.04 Install Process
(tested on FRESH install of ubuntu 16.04 Installed PYTHON3.5, Pip3 and below)

  
  ```bash
  git clone the repository and cd into it  
  
  sudo apt install python3.5  
  
  Sudo apt install python3-pip  
  
  pip3 install splinter  
  
  pip3 install pygeocoder  #(MAY NEED to use sudo -H pip3 install pygeocoder)  
  
  chmod +x installphantomjs.sh  
  
  sudo ./installphantomjs.sh
  ```
ON UBUNTU 16.04 A Script was Found [here](https://gist.github.com/julionc/7476620) This script was made by [gautiermichelin](https://gist.github.com/gautiermichelin) props to him 

Running the Program

In the directory this was cloned to.
```bash
python3.5 address.py 

Starting Address in Quotes "1600 Pennsylvania Ave NW, Washington, DC 20006"

It will ask a range, Valid answers are 100-1600 (Meters: 1600 Meters is 1 Mile)

run address.py and give it a starting address and a radius in meters to search within.  
Starting Address in Quotes "1600 Pennsylvania Ave NW, Washington, DC 20006"

After this is complete, a file (addresses) will be there.

python3.5 speedcheck.py

It will ask for the state.  Type in the 2 Letter State
```


use http://www.easymapmaker.com to create the map from the results file

The code probably needs lots of clean up. I have never programmed in Python until yesterday so forgive me for inaccuracies.
I am just glad I was able to port this over from the Century Link folks on dslr.

Anyone is welcome to modify and improve the code.
