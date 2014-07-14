'''
Copyright (C) 2014 Cisco Systems Inc.
  Modified : NetworkZIGI (2014.07.15)
'''
import re
import cisco
import sys
from argparse import ArgumentParser

def checkRange(checkIP):
    octets = checkIP.split('.')
    for octet in octets:
        ip = int(octet)
        if (ip < 0 or ip > 255):
            print "Invalid Input Value"
            print "IP value is not less than 0 or greater than 255."
            sys.exit()

    return True


def expandrange(rangefunc,stepcnt):
    hosts = []
    step = str(stepcnt[0])
    octets = rangefunc.split('.')
    for i,octet in enumerate(octets):
        if '-' in octet:
            octetrange = octet.split('-')
            sip = int(octetrange[0])
            dip = int(octetrange[1])

            for digit in range(int(octetrange[0]),int(octetrange[1])+1, int(step) if i==3 else 1):
                ip = '.'.join(octets[:i] + [str(digit)] + octets[i+1:])
                hosts += expandrange(ip,stepcnt)
            break
    else:
        if checkRange(rangefunc):
            hosts.append(rangefunc)
    return hosts

parser = ArgumentParser('AdvPing')
parser.add_argument('ip', help='IP range to ping, e.g., 10.1.0-1.0-255 will expand to 10.1.0.0/23')
parser.add_argument('options', type=str, default=['1'], nargs='*', help='Options to pass to ping')
args = parser.parse_args()
targets = expandrange(args.ip,args.options)

for ip in targets:
    tupleping  = cisco.cli('ping %s' % ip)
    strping = str(tupleping)
    m = re.search('([0-9\.]+)% packet loss',strping )
    print('%s - %s' % (ip, 'UP' if float(m.group(1)) == 0.0 else 'DOWN'))
