#I've tested with  Nexus7010-version 6.2(8) this code. 
#When a user enters a IP, you can check the MAC / VLAN / Interface / Description information.

#Example Result)
#NEXUS-7K# python ipinfo.py 10.10.10.12
#10.10.10.12 : Not found IP Address Infomation

#NEXUS-7# python ipinfo.py 10.10.10.11
#================================================
#      IP Info : NetworkZIGI   2014.07.19        
#================================================
#IP-Address      : 10.10.10.11
#Mac-Address     : 0012.3456.789A
#Vlan            : 20
#Interface       : E12/3
#Description     : NetworkZIGI Blog Web Server
#
#!/bin/env python 
import argparse 
import sys  
import cisco  
IP = 'IP-Address'  
MAC = 'Mac-Address'  
Vlan = 'Vlan'  
Intf = 'Interface'  
Desc = 'Description'  
IP_info = {IP:'None', MAC:'None', Vlan:'None', Intf:'None', Desc:'None'}  

def get_ARP_Table(ipaddr):  
    arpCmd = 'sh ip arp ' + ipaddr  
    arpCmdResult = cisco.cli(arpCmd)  
    arpCmdResultList = arpCmdResult.split('\n')  
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
    macCmdResult = cisco.cli(macCmd)  
    macCmdResultList = macCmdResult.split('\n')  
 
    for infInfo in macCmdResultList:  
        idx = infInfo.find(IP_info[MAC])  
        if(-1<idx):  
            IP_info[Intf] = infInfo[58:]  
            get_Description_info(IP_info[Intf])  
            break  


def get_Description_info(iInfo):  
    if(iInfo.find('Eth') == 0 or iInfo.find('Po')==0):   
        intCmd = 'sh int desc | inc ' + iInfo  
        intCmdResult = cisco.cli(intCmd)  
        if(intCmdResult != ''):  
            intCmdResultList = intCmdResult.split('\n')  
            IP_info[Desc] = intCmdResultList[0][25:].strip()  

def show_IP_info():  
    print '================================================'  
    print '             IP Info : NetworkZIGI              '  
    print '================================================'  
    print '%-15s : %s' % (IP,IP_info[IP])  
    print '%-15s : %s' % (MAC,IP_info[MAC])  
    print '%-15s : %s' % (Vlan, IP_info[Vlan])  
    print '%-15s : %s' % (Intf, IP_info[Intf])  
    print '%-15s : %s' % (Desc,IP_info[Desc])  

parser = argparse.ArgumentParser('Args',description='Args Desc')  
parser.add_argument('ip')  
args = parser.parse_args()  

iparp = get_ARP_Table(args.ip)  
get_IP_MAC_info(iparp)  
get_Interface_info()  
show_IP_info()  
