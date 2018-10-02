from telnetlib import Telnet

h,l,p="sw3115","locator","good&flow!"

try:
    tn = Telnet(h)
except:
    print "Connection Failed"


tn.write(l+"\n")#this is the username

tn.write(p+"\n")#this is the password
