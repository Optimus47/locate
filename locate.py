from telnetlib import Telnet
from requests.exceptions import ConnectionError


try:
    tn = Telnet(HOST)
except:
    print "Connection Failed"


tn.write("hello")#this is the username

tn.write("hello@123")#this is the password
