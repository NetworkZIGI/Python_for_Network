__author__ = 'Network ZIGI - Ko Jae Sung'
# 2014.08.18. First Version
#
#This Program runs on the Nexus 7K and Nexus 5K.
#This Program requires vCheck Module for Nexus Version Checking.
#You can see vCheck Module in NetworkZIGI Github.
#Check the Nexus Version with vCheck Module before program execution. 
#According to the identified Nexus Version, and executes the appropriate code.
#
#===================================
#  enhanced IP Info : NetworkZIGI      
#===================================
#IP-Address      : 10.0.0.1
#Mac-Address     : 0012.3456.abcd
#Vlan            : 11
#Interface       : Eth14/2
#Description     : NetworkZIGI Blog Server
#
# Blog : http://ThePlmingspace.tistory.com
# 
# Tested : Cisco Nexus 7010  : 6.2.(8)
# Tested : Cisco Nexus 5548  : 6.0(2)N2(4)


#!/bin/env python 
import argparse
import sys
import cisco
import vCheck
from vCheck import NexusVersionCheck

# Constant
IP = 'IP-Address'
MAC = 'Mac-Address'
Vlan = 'Vlan'
Intf = 'Interface'
Desc = 'Description'


IP_info = {IP:'None', MAC:'None', Vlan:'None', Intf:'None', Desc:'None'}
NexusVersion = ''

def get_ARP_Table(ipaddr):
    arpCmd = 'sh ip arp ' + ipaddr
    arpCmdResultList = [] 
    if(vCheck.NexusVersion==vCheck.N7K):
        arpCmdResult = cisco.cli(arpCmd)
        arpCmdResultList = arpCmdResult.split('\n')
    elif(vCheck.NexusVersion==vCheck.N5K):
        arpCmdResult = cisco.CLI(arpCmd, False)
        arpCmdResultList = arpCmdResult.get_output()

    for arp in arpCmdResultList:
        if (-1<arp.find(args.ip)):
            return arp
    else:
        print ' %s : Not found IP Address Infomation' % args.ip
        sys.exit()

def get_IP_MAC_info(info):
    info_list = info.split()
    IP_info[IP] = info_list[0]
    IP_info[MAC] = info_list[2]
    IP_info[Vlan] = info_list[3][4:]

def get_Interface_info():
    macCmd = 'sh mac address-table addr ' + IP_info[MAC]
    macCmdResultList = [] 
    if(vCheck.NexusVersion==vCheck.N7K):
        macCmdResult = cisco.cli(macCmd)
        macCmdResultList = macCmdResult.split('\n')
    elif(vCheck.NexusVersion==vCheck.N5K):
        macCmdResult = cisco.CLI(macCmd, False)
        macCmdResultList = macCmdResult.get_output()

    for infInfo in macCmdResultList:
        idx = infInfo.find(IP_info[MAC])
        if(-1<idx):
            IP_info[Intf] = infInfo[58:]
            get_Description_info(IP_info[Intf])
            break


def get_Description_info(iInfo):
    if(iInfo.find('Eth') == 0 or iInfo.find('Po')==0):
        intCmd = 'sh int desc | inc ' + iInfo
        if(vCheck.NexusVersion==vCheck.N7K):
            intCmdResult = cisco.cli(intCmd)
            intCmdResultList = intCmdResult.split('\n')
            if(intCmdResult != ''):
                IP_info[Desc] = intCmdResultList[0][25:].strip()
        elif(vCheck.NexusVersion==vCheck.N5K):
            intCmdResult = cisco.CLI(intCmd, False)
            intCmdResultList = intCmdResult.get_output()
            if(intCmdResult != ''):
                IP_info[Desc] = intCmdResultList[0][25:].strip()

def show_IP_info():
    print '==================================='
    print '  enhanced IP Info : NetworkZIGI   '
    print '==================================='
    print '%-15s : %s' % (IP,IP_info[IP])
    print '%-15s : %s' % (MAC,IP_info[MAC])
    print '%-15s : %s' % (Vlan, IP_info[Vlan])
    print '%-15s : %s' % (Intf, IP_info[Intf])
    print '%-15s : %s' % (Desc,IP_info[Desc])

NexusVersionCheck()">> eipinfo.py
parser = argparse.ArgumentParser('Args',description='Args Desc')
parser.add_argument('ip')
args = parser.parse_args()
iparp = get_ARP_Table(args.ip)
get_IP_MAC_info(iparp)
get_Interface_info()
show_IP_info()
