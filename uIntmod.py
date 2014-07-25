# -*- coding: utf-8 -*-
__author__ = 'Network ZIGI'
# 2014.07.25. First Version (Only Cisco Nexus)
# Example>
#NX-OS# python
#Python 2.7.2 (default, Nov 27 2012, 17:50:33)
#[GCC 4.3.2] on linux2
#Type "help", "copyright", "credits" or "license" for more information.
#Loaded cisco NxOS lib!
#>>> import uIntmod
#>>> uIntmod.rate('po1',5,2)
#  1 >> [ Input ]          9592 bps -       9 pps : [ Ouput ]        126888 bps  -     173 pps  [ 30 seconds]
#  2 >> [ Input ]          9264 bps -       9 pps : [ Ouput ]        125600 bps  -     170 pps  [ 30 seconds]
#  3 >> [ Input ]          9264 bps -       9 pps : [ Ouput ]        125600 bps  -     170 pps  [ 30 seconds]
#  4 >> [ Input ]          9264 bps -       9 pps : [ Ouput ]        125600 bps  -     170 pps  [ 30 seconds]
#  5 >> [ Input ]          9328 bps -       9 pps : [ Ouput ]        124000 bps  -     166 pps  [ 30 seconds]
#===========================================================================
#Max  >> [ Input ]          9592 bps -       9 pps : [ Ouput ]        126888 bps  -     173 pps
#>>> exit()
#NX-OS#
#
# Blog : http://ThePlmingspace.tistory.com
#
# The module shows the amount of input and output interfaces.
# When you enter the desired  'time interval'/'repeats', shows the result.
# This module is run in 'Cisco Python Shell mode'.
# 'Cisco Cli Mode' is shown after the end of the Program, but Shell mode shown result promptly
# When used in shell mode, you can run after you import the module.
# Tested : Cisco Nexus 5548  : 6.0(2)N2(4)

import cisco
import time
from argparse import ArgumentParser

def CheckInterfaceRate(args):
    inPacketList = []
    inBitList =[]
    outPacketList=[]
    outBitList=[]

    for cnt in range(1,args['repeat']+1):
        result = getInterfaceRate(args['intInfo'])
        print '%8d >>  [ Input ]  %13s bps -  %6s pps   :   [ Ouput ]  %13s bps  -  %6s pps    [ %s %s]' % \
        (cnt,result[0][4], result[0][6],result[1][4],result[1][6],result[0][0],result[0][1])
        inBitList.append(int(result[0][4]))
        inPacketList.append(int(result[0][6]))
        outBitList.append(int(result[1][4]))
        outPacketList.append(int(result[1][6]))
        time.sleep((args['interval']))

    print '==========================================================================='
    print 'Max  >>   [ Input ]  %13d bps -  %6d pps   :   [ Ouput ]  %13d bps  -  %6d pps ' % \
    (max(inBitList), max(inPacketList),max(outBitList), max(outPacketList))

def getInterfaceRate(): #(Intinfo)
    intRateCmdResult =cisco.CLI('sh int '+Intinfo,False)
    intRateCmdResultList =intRateCmdResult.get_output()
    for rate in intRateCmdResultList:
        if(-1<rate.find('input rate')):
            inputList = rate.split()
        elif ( -1<rate.find('output rate')):
            outputList = rate.split()
            return inputList, outputList

def rate(info,r,step=1):
    args = {'intInfo':info,'repeat': r, 'interval':step}
    CheckInterfaceRate(args)
