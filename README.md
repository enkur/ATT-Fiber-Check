# ATT-Fiber-Check
program to check where Fiber is available

Credit to MTdoyle for the original Century Link  speed checker
https://github.com/mtdoyle/cl_speedcheck

Requires Python 3.6  
  
If running 
splinter package (pip install splinter)  
phantomjs web driver  




ON UBUNTU 16.04 A Script was Found [here](https://gist.github.com/julionc/7476620)
pygeocoder package (pip install pygeocoder)

```bash
#!/usr/bin/env bash
# This script install PhantomJS in your Debian/Ubuntu System
#
# This script must be run as root:
# sudo sh install_phantomjs.sh
#

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

PHANTOM_VERSION="phantomjs-2.1.1"
ARCH=$(uname -m)

if ! [ $ARCH = "x86_64" ]; then
    $ARCH="i686"
fi

PHANTOM_JS="$PHANTOM_VERSION-linux-$ARCH"

apt-get update
apt-get -y install build-essential chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev

cd ~
wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2
tar xvjf $PHANTOM_JS.tar.bz2
mv $PHANTOM_JS /usr/local/share/
ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/share/phantomjs
ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin/phantomjs
ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/bin/phantomjs
```

run address.py and give it a starting address and a radius in meters to search within.  
Starting Address in Quotes "1600 Pennsylvania Ave NW, Washington, DC 20006"

These results are written to a file 
give a minimum of 100 meters. 1600 meters(1 mile) resulted in 400 addresses so be careful.

run speedcheck.py to query the addresses with AT&T and will report back if Fiber is available and if not then what other speeds are offered.

use http://www.easymapmaker.com to create the map from the results file

The code probably needs lots of clean up. I have never programmed in Python until yesterday so forgive me for inaccuracies.
I am just glad I was able to port this over from the Century Link folks on dslr.

Anyone is welcome to modify and improve the code.
