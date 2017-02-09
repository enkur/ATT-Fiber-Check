# ATT-Fiber-Check
program to check where Fiber is available

Credit to MTdoyle for the original Century Link  speed checker
https://github.com/mtdoyle/cl_speedcheck

Requires Python 3.6
splinter package (pip install splinter)
chrome web driver


run address.py and give it a starting NE address and ending SW address. It will find all the addresses within the box and save it to file called addresses

run speedcheck.py to query the addresses with AT&T and will report back if Fiber is available and if not then what other speeds are offered. Numbers returned are 1000,... 0 (0 means no service)

use http://www.easymapmaker.com to create the map from the results file

The code probably needs lots of clean up. I have never programmed in Python until yesterday so forgive me for inaccuracies.
I am just glad I was able to port this over from the Century Link folks on dslr.

Anyone is welcome to modify and improve the code.
