from telnetlib import Telnet
#from netmiko import ConnectHandler

h,l,p="sw3115","locator","good&flow!"
COMMAND="dis clock"

with telnetlib.Telnet(h) as t:
    t.read_until(b'Username:')
    t.write(l + b'\n')

    t.read_until(b'Password:')
    t.write(p + b'\n')
#    t.write(b'enable\n')

#    t.read_until(b'Password:')
#    t.write(ENABLE_PASS + b'\n')
#    t.write(b'terminal length 0\n')
    t.write(COMMAND + b'\n')

    time.sleep(5)

    output = t.read_very_eager().decode('utf-8')
    print(output)
    
## old Connection

#tn.write(l+"\n")#this is the username

#tn.write(p+"\n")#this is the password
