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
switches=['sw3115','sw1211','sw1141','sw1221','sw1322','sw1541','sw1571','sw1361','sw1641','ilo1652']
l,p="locator","good&flow!"

#mac_addr="00:00:5E:00:01:4D"

mac_addr_plain = mac_addr.replace(':', '').lower()
mac_addr_hp = '-'.join(mac_addr_plain[i:i+4] for i in range(0,11,4))
mac_addr_cisco = mac_addr_hp.replace('-','.')

print mac_addr, mac_addr_plain, mac_addr_hp, mac_addr_cisco

print "Locate on",len(switches),"h3c switches"
for h in switches:
    print "Switch",h
    try:
        tn = telnetlib.Telnet(h, timeout=10)
        tn.read_until(b'Username:')
        tn.write(l + b'\n')
        tn.read_until(b'Password:')
        tn.write(p + b'\n')
        tn.read_until(finish)
        tn.write('screen-length disable' + '\n')
        tn.read_until(finish)
        tn.write('dis mac-address ' + mac_addr_hp + '\n')
        #tn.interact()
        mac_table = tn.read_until(finish)

        mac_port = re.findall('GigabitEthernet\d/\d/\d{,2}',mac_table)

        for port in mac_port:
            tn.write('dis cur int ' + port + '\n')
            tn.read_until(config)
            print tn.read_until(config)
            tn.read_until(finish)

    except:
        print "Error connecting to host", h
