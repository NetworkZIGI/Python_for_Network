# -*- coding: utf-8 -*-
__author__ = 'Network ZIGI'
# 2014.07.25. First Version (Only Cisco Nexus)
# Example>
# NX-OS# python uInt.py po1 5 2
#  1 >> [ Input ]          9592 bps -       9 pps : [ Ouput ]        126888 bps  -     173 pps  [ 30 seconds]
#  2 >> [ Input ]          9264 bps -       9 pps : [ Ouput ]        125600 bps  -     170 pps  [ 30 seconds]
#  3 >> [ Input ]          9264 bps -       9 pps : [ Ouput ]        125600 bps  -     170 pps  [ 30 seconds]
#  4 >> [ Input ]          9264 bps -       9 pps : [ Ouput ]        125600 bps  -     170 pps  [ 30 seconds]
#  5 >> [ Input ]          9328 bps -       9 pps : [ Ouput ]        124000 bps  -     166 pps  [ 30 seconds]
#===========================================================================
#Max  >> [ Input ]          9592 bps -       9 pps : [ Ouput ]        126888 bps  -     173 pps
#
# Blog : http://ThePlmingspace.tistory.com
#
# The module shows the amount of input and output interfaces.
# When you enter the desired  'time interval'/'repeats', shows the result.
# But, Cisco Cli mode shown after the end of the Program
# So, If you enter 'interval time 3/ repeat 3', the result shows that after 9 seconds.
#
# Tested : Cisco Nexus 5548  : 6.0(2)N2(4)


import cisco
import sys
import time
from argparse import ArgumentParser 

def CheckInterfaceRate():

    inPacketList = []
    inBitList =[]
    outPacketList=[]
    outBitList=[]

    for cnt in range(1,int(args.repeat)+1): 
        result = getInterfacerRate()        
        print '%8d >>  [ Input ]  %13s bps -  %6s pps   :   [ Ouput ]  %13s bps  -  %6s pps    [ %s %s]' % \
        (cnt,result[0][4], result[0][6],result[1][4],result[1][6],result[0][0],result[0][1])
          
        inBitList.append(int(result[0][4]))        
        inPacketList.append(int(result[0][6]))
        outBitList.append(int(result[1][4]))
        outPacketList.append(int(result[1][6]))
        time.sleep(int(args.interval[0]))           

    print '==========================================================================='
    print 'Max  >>   [ Input ]  %13d bps -  %6d pps   :   [ Ouput ]  %13d bps  -  %6d pps ' % \
    (max(inBitList), max(inPacketList),max(outBitList), max(outPacketList))


def getInterfacerRate():
    intRateCmdResult = cisco.CLI('sh int '+args.Intinfo, False) 
    intRateCmdResultList =intRateCmdResult.get_output() 
    for rate in intRateCmdResultList:  
        if(-1<rate.find('input rate')):
            inputList = rate.split()  
        elif ( -1<rate.find('output rate')):  
            outputList = rate.split()          
            return inputList, outputList  

parser = ArgumentParser('usingInt')
parser.add_argument('Intinfo',  help='Interface')
parser.add_argument('repeat', help='repeat Interface Input/Output rate')
parser.add_argument('interval', type=str, default=['1'],nargs='*',  help='Interval time (Second) - [default : 1 Second]')
args = parser.parse_args()
CheckInterfaceRate()

