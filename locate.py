import telnetlib
import time
import re
import argparse
from getmac import get_mac_address

parser = argparse.ArgumentParser()
parser.add_argument('-ip', help='Locate ip')
args = parser.parse_args()

print args.ip
mac_addr = get_mac_address(ip=args.ip)

finish,config = '>','#'
switches=[ 'ilo1212', 'sw3115' ]
#,'sw1211','sw1141','sw1221','sw1322',
#            'sw1541','sw1571','sw1361','sw1641','ilo1652']
l,p,sp="locator","good&flow!","rolo"

#mac_addr="00:00:5E:00:01:4D"
mac_addr_hp="3822-d62c-1b37"

mac_addr_plain = mac_addr.replace(':', '').lower()
mac_addr_hp = '-'.join(mac_addr_plain[i:i+4] for i in range(0,11,4))
mac_addr_cisco = mac_addr_hp.replace('-','.')

###DEBUG
mac_addr_hp="3822-d62c-1b37"

print mac_addr, mac_addr_plain, mac_addr_hp, mac_addr_cisco

print "Locate on",len(switches),"h3c switches"
for h in switches:
    isCisco = 0
    finish = '>'
    print "Switch",h
    try:
        tn = telnetlib.Telnet(h, timeout=10)
        banner = tn.read_until(b'Username:')
        if re.findall("User Access Verification",banner):
#            tn.read_until(b' ')
            print "CISCO!"
            isCisco = 1
#
        tn.write(l + b'\n')
        tn.read_until(b'Password:')
        tn.write(p + b'\n')
#        tn.interact()
        tn.read_until(finish)
        if isCisco:
            tn.write('term len 0' + '\n')
            tn.read_until(finish)
            tn.write('en' + '\n')
            tn.read_until(b'Password: ')
            tn.write(sp + b'\n')
            finish='#'
            tn.read_until(finish)
            tn.write('sh mac add add ' + mac_addr_cisco + '\n')
#            mac_table =tn.read_until('#')
        else:
#            tn.interact()
            tn.write('screen-length disable' + '\n')
            tn.read_until(finish)
            tn.write('dis mac-address ' + mac_addr_hp + '\n')


        mac_table = tn.read_until(finish)

#        tn.interact()

        mac_port_cisco = re.findall('[G|F][i|o]\d/\d{,2}',mac_table)
        mac_port = re.findall('GigabitEthernet\d/\d/\d{,2}',mac_table)

        if isCisco:
            for port in mac_port_cisco:
                print h,port
                tn.write('sh run int ' + port + '\n')
                config = tn.read_until(finish)

        else:
            for port in mac_port:
                tn.write('dis cur int ' + port + '\n')
                config = tn.read_until(finish)
                #tn.interact()
                #print tn.read_until(config)
                #tn.read_until(finish)

        print config

    except:
        print "Error connecting to host", h
