#python imports
import sys
import os
import subprocess
from termcolor import colored

#third-party imports
#No third-party imports

#programmer generated imports
from logger import logger
from fileio import fileio

'''
***BEGIN DESCRIPTION***
Executes a grep against the abuse.ch ransomware URLs feed.
***END DESCRIPTION***
'''
def POE(logdir, target, logging, debug):

    if (logging == True): 
        LOG = logger() 
    newlogentry = ''
    alx_output_data = ''
    output = logdir + 'Abuse_ch_ransomware_URLs.txt'
    malware_flag = 0

    if (target.ip == True):
        print colored('\r\n[-] Unable to execute abuse.ch ransomware URL grep - target must be a domain or URL - skipping.', 'yellow', attrs=['bold']) 
        if (logging == True):
            newlogentry = 'Unable to execute abuse.ch ransomware URL grep - target must be a domain or URL - skipping.'
            LOG.WriteLog(logdir, target.target, newlogentry)
        return -1

    FI = fileio()

    print '\r\n[*] Running abuse.ch ransomware URL grep against: ' + target.target

    subproc = subprocess.Popen('grep ' + target.target + ' /opt/mirage/feeds/RW_URLBL.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for alx_data in subproc.stdout.readlines():
        if (alx_data != ''):
            target.abuse_ch_ransomware_urls = True
            malware_flag = 1
            print colored('[-] Target appears in the abuse.ch ransomware URL feed', 'red', attrs=['bold'])
        if (debug == True):
            print '[DEBUG]: ' + alx_data 
        alx_output_data += alx_data 
    
    if (alx_output_data != ''):                      
        try:        
            FI.WriteLogFile(output, alx_output_data)
            print colored('[*] abuse.ch ransomware URL data had been written to file here: ', 'green') + colored(output, 'blue', attrs=['bold'])
            if (logging == True):
                newlogentry = 'abuse.ch ransomware URL data has been generated to file here: <a href=\"' + output + '\"> abuse.ch ransomware Output </a>'
                LOG.WriteLog(logdir, target.target, newlogentry)
                if (malware_flag == 1):
                    newlogentry = '|-----------------> Target appears in the abuse.ch feed'
                    LOG.WriteLog(logdir, target.target, newlogentry)

        except:
            print colored('[x] Unable to write abuse.ch ransomware URL data to file', 'red', attrs=['bold']) 
            if (logging == True):
                newlogentry = 'Unable to write abuse.ch ransomware URL data to file'
                LOG.WriteLog(logdir, target.target, newlogentry)
            return -1
    else:
        print colored('[-] Target does not appear in the abuse.ch ransomware URL feed', 'yellow', attrs=['bold'])    
        print colored('[x] abuse.ch ransomware URL data not written to file', 'red', attrs=['bold'])

    return 0
