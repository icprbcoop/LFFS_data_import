#!/usr/bin/python
############################################################
#
# Make connection to the FEWS PI and Retrieve NLDAS grb files
#
# Script developed by Riverside Technology, Inc.
#       2013-10-18      ism,csd,hsk for ICPRB
#
############################################################

from suds.client import Client
import sys
import urllib2
import FEWSConnect
import logging
import datetime
import time

#t0=time.time()

from cookielib import CookieJar
from urllib import urlencode

username = "icprb"
password = "NorthBranch1"

# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login
 
password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)

cookie_jar = CookieJar()

opener = urllib2.build_opener(
    urllib2.HTTPBasicAuthHandler(password_manager),
    #urllib2.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib2.HTTPSHandler(debuglevel=1),   # details of the requests/responses
    urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)

# note that last 4 digits of local host may depend on what FEWS license
# is open (e.g. 8100, 8101) - check in log window during FEWS start up

FEWSServer = sys.argv[2]
WSDLLocation = 'FewsPiService?WSDL'


if (__name__ == '__main__'):
    serverString = 'http://' + FEWSServer + '/' + WSDLLocation
    cnxn = Client(serverString)

# parse the run_info.xml file
    runInfoFile = sys.argv[1]
    [runInfo,  key, value] = FEWSConnect.parseRunInfo(runInfoFile)

# start the log file
    logFile = runInfo['outputDiagnosticFile'].rstrip('.xml') + '.txt'
    FEWSConnect.initLogging(logFile)
    log=logging.getLogger()
    log.debug('Opened log file: %s', logFile)
    log.info('Successfully parsed %s', runInfoFile)

# retrieve and define properties from FEWS run_info.xml
    try:
            importDir = None
            archiveDir = None
            lookback = None
            host = None
            for i in range(0,len(key)):
                if (key[i].upper() == 'IMPORTDIR'):
                    importDir = value[i]
                elif (key[i].upper() == 'ARCHIVEDIR'):
                    archiveDir = value[i]
                elif (key[i].upper() == 'LOOKBACK'):
                    lookback = value[i]
                elif (key[i].upper() == 'HOST'):
                    host = value[i]
    except:
                log.warning('Could not initialize variables')
                FEWSConnect.logFileToXML(logFile, runInfo['outputDiagnosticFile'])
                sys.exit()
                
# Check if host site is available to retrieve NLDAS files from ftp.  Try 5 times
    success = False
    tries = 1
    while not success and tries < 6:
        try:
            tresponse = urllib2.urlopen(host)
            html = tresponse.read()
            log.debug('Connected to host %s in %s tries', host, tries)
            print('Connected to host'+host+' in '+str(tries) +' tries')
            success = True
        except:
            if tries == 5:
                log.warning('Could not connect to host %s in 5 tries', host)
                print('Could not connect to host '+host+' in 5 tries')
                FEWSConnect.logFileToXML(logFile, runInfo['outputDiagnosticFile'])
                sys.exit()
            time.sleep(1)
            tries += 1

# Check directories with files starting at lookback time in days from current date
# grb files contained in directories defined by year/day of year
    lookback = int(lookback)
    for lookback in xrange(lookback,4,-1):
        startDownload =  datetime.datetime.utcnow() - datetime.timedelta(days=int(lookback))
        year = startDownload.year
        dayofyear= startDownload.strftime('%j')
        print dayofyear
        ftp=host+str(year)+'/'+str(dayofyear)+'/'
        try:
            response = urllib2.urlopen(ftp)

# Script will check for directories of data from lookback upto present time
# warnings provided to FEWS if no data is available (eariest data typically 5-3 days back)
        except:
            downloaddate=datetime.datetime.strftime(startDownload, '%Y-%m-%d')
            print ('No data available for NLDAS grid on '+downloaddate)
            log.warning('No data available for NLDAS grids on %s', downloaddate)
            continue

#from julian day to date
	#test=12
	h=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	list_h=[]
	for test in h:
		#test1='00%s'%str(test)
		#print test1
		test2=str(test).zfill(2)
		test3='%s00'%str(test2)
		#print test2
	#print testlist
	#print test
	#date = datetime.datetime (year,1,1) + datetime.timedelta(dayofyear)
	#print date
		date = datetime.datetime(year,1,1) + datetime.timedelta(int(dayofyear)-1)
		dateformat = 'NLDAS_FORA0125_H.A%s.%s.002.grb'%(date.strftime('%Y%m%d'),test3)
	#print date
		#print dateformat
		list_h.append(dateformat)
	#print list_h

# If data is available read the FTP and split lines to retrieve grb filenames
        #HTMLPage =response.read()
        #s = HTMLPage.split('\n')
        #list = ["NLDAS_FORA0125_H.A20170108.0000.002.grb"]
        #print list
        #print s
# Create list of .grb file names to retrieve from site checking line by line
        #list = [filename for filename in (line.strip().split()[8]
        #                                       for line in s if line.strip())
        #             if filename.endswith('grb')]

# Read and write each available file from list to FEWS importDir
        for file in list_h:
            #print file
	    #print (ftp+file)
	    request = urllib2.Request(ftp+file)
	    response = urllib2.urlopen(request)
            grib = response.read()
#grib = urllib2.urlopen(ftp+file).read()
#            Store file in FEWS import Directory
            with open(importDir+file, 'wb') as f:
                f.write(grib)
#            Store file in Archive Directory - TEMPORARILY SUSPEND
#            with open(archiveDir+file, 'wb') as a:
#                a.write(grib)


    FEWSConnect.logFileToXML(logFile, runInfo['outputDiagnosticFile'])

#t1=time.time()
#total=t1-t0
#print total

