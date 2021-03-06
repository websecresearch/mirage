#python imports
import sys
import os
import subprocess
import json
import simplejson
import urllib
import urllib2
from termcolor import colored

#third-party imports
#No third-party imports

#programmer generated imports
from logger import logger
from fileio import fileio

'''
***BEGIN DESCRIPTION***
Type: Info - Description: Retrieves the reputation data for domains and IPs against the VirusTotal database.
***END DESCRIPTION***
'''
def POE(POE):

    #Add your VirusTotal API key inside the quotes on the line below <--------------------------
    apikey = ''

    if (POE.logging == True): 
        LOG = logger() 
    newlogentry = ''
    reputation_dump = ''
    reputation_output_data = ''
    vt = ''

    if (apikey == ''):
        print colored('\r\n[x] Unable to execute VirusTotal reputation module - apikey value not input.  Please add one to /opt/mirage/modules/VTReputation.py', 'red', attrs=['bold']) 
        if (logging == True):
            newlogentry = 'Unable to execute VirusTotal reputation module - apikey value not input.  Please add one to /opt/mirage/modules/VTReputation.py'
            LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            POE.csv_line += 'N/A,'
        return -1

    global json
    malware_flag = 0
    badware_flag = 0
    infection_flag = 0
    output = POE.logdir + 'VTReputation.json'

    FI = fileio()
    
    print '\r\n[*] Running VT reputation against: ' + POE.target

    if (POE.url == True):
        vt = "https://www.virustotal.com/vtapi/v2/url/report"
        parameters = {"resource": POE.target, "apikey": apikey.rstrip('\n')}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(vt, data)
        response = urllib2.urlopen(req)
        json = response.read()
        if (POE.debug == True):
            print json
        response_dump = json.dumps(response)
    elif (POE.domain == True):
        vt = "http://www.virustotal.com/vtapi/v2/domain/report"
        parameters = {"domain": POE.target, "apikey": apikey.rstrip('\n')}
        response = urllib.urlopen('%s?%s' % (vt, urllib.urlencode(parameters))).read()
        response_dict = json.loads(response)
        if (POE.debug == True):
           print response_dict
        response_dump = json.dumps(json.JSONDecoder().decode(response), sort_keys=True, indent = 4)
    else:
        vt = "http://www.virustotal.com/vtapi/v2/ip-address/report"
        parameters = {"ip": POE.target, "apikey": apikey.rstrip('\n')}
        response = urllib.urlopen('%s?%s' % (vt, urllib.urlencode(parameters))).read()
        response_dict = json.loads(response)
        if (POE.debug == True):
           print response_dict
        response_dump = json.dumps(json.JSONDecoder().decode(response), sort_keys=True, indent=4)

    if (response_dump.find('seen to host badware')!= -1):
        malware_flag = 1             
    elif (response_dump.find('known infection source')!= -1): 
        malware_flag = 1            

    if (malware_flag == 1):
        POE.VT = True
        print colored('[-] Target has been flagged for malware', 'red', attrs=['bold'])  
    else:
        print colored('[*] Target has not been flagged for malware', 'green', attrs=['bold'])  
   
    try:        
        FI.WriteLogFile(output, response_dump)
        print colored('[*] VirusTotal reputation data had been written to file here: ', 'green') + colored(output, 'blue', attrs=['bold'])
        if (POE.logging == True):
            newlogentry = 'VirusTotal data has been generated to file here: <a href=\"' + output + '\"> VirusTotal Reputation Output </a>'           
            LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            if ((malware_flag == 1) and (badware_flag == 1) and (infection_flag == 1)):
                newlogentry = '<strong>|-----------------> Target has been flagged for malware, has been seen to host badware and is a known infection source </strong>'
                POE.csv_line += 'Malware/Subdomains/Infection_Source,'
                LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            elif ((malware_flag == 1) and (badware_flag == 1) and (infection_flag == 0)):
                newlogentry = '<strong>|-----------------> Target has been flagged for malware and has been seen to host badware</strong>'
                POE.csv_line += 'Malware/Badware,'
                LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            elif ((malware_flag == 1) and (badware_flag == 0) and (infection_flag == 1)):
                newlogentry = '<strong>|-----------------> Target has been flagged for malware and is a known infection source</strong>'
                POE.csv_line += 'Malware/Infection_Source,'
                LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            elif ((malware_flag == 1) and (badware_flag == 0) and (infection_flag == 0)):
                newlogentry = '<strong>|-----------------> Target has been flagged for malware</strong>'
                POE.csv_line += 'Malware,'
                LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            elif ((malware_flag == 0) and (badware_flag == 1) and (infection_flag == 0)):
                newlogentry = '<strong>|-----------------> Target has been seen to host badware</strong>'
                POE.csv_line += 'Badware,'
                LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            elif ((malware_flag == 0) and (badware_flag == 0) and (infection_flag == 1)):
                newlogentry = '<strong>|-----------------> Target is a known infection source</strong>'
                POE.csv_line += 'Infection_Source,'
                LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            else:
                POE.csv_line += 'False,'
    except:
        print colored('[x] Unable to write VirusTotal reputation data to file', 'red', attrs=['bold']) 
        if (POE.logging == True):
            newlogentry = 'Unable to write VirusTotal reputation data to file'
            LOG.WriteLog(POE.logdir, POE.target, newlogentry)
            POE.csv_line += 'N/A,'
        return -1

    return 0
