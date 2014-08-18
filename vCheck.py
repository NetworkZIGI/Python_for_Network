__author__ = 'Network ZIGI - Ko Jae Sung'
#This Module used to Check Version of  Nexus.
#In fact, It can only be checked whether Nexus 7K or not.
#!/bin/env python 
import sys 
N7K = 'Nexus7000' 
N5K = 'Nexus5000' 
#N3K = 'Nexus3000'     : Constant for Extension.

NexusVersion = ''

def NexusVersionCheck():
    global NexusVersion 
    sysPathList = sys.path
    for pathItem in sysPathList:
        if(pathItem=='/bootflash/scripts'):
            NexusVersion = N7K
            break
    else:
        NexusVersion = N5K

if __name__ == '__main__':
    NexusVersionCheck()
    print NexusVersion
