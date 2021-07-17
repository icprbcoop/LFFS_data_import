#!/usr/bin/python
############################################################
#
# Make connection to the FEWS PI and Retrieve MARFC files
#
# Script developed by Riverside Technology, Inc.
#       2013-10-18      ism,csd,hsk for ICPRB
#
############################################################


from suds.client import Client
from traceback import format_exc
import sys
import FEWSConnect
import logging
from paramiko import Transport
from paramiko import SFTPClient



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
            host = None
            port = None
            usr = None
            pw = None
            path = None
            lookback = None
            for i in range(0,len(key)):
                if (key[i].upper() == 'IMPORTDIR'):
                    importDir = value[i]
                elif (key[i].upper() == 'ARCHIVEDIR'):
                    archiveDir = value[i]
                elif (key[i].upper() == 'HOST'):
                    host = value[i]
                elif (key[i].upper() == 'PORT'):
                    port = value[i]
                elif (key[i].upper() == 'USR'):
                    usr = value[i]
                elif (key[i].upper() == 'PW'):
                    pw = value[i]
                elif (key[i].upper() == 'PATH'):
                    path = value[i]
                elif (key[i].upper() == 'LOOKBACK'):
                    lookback = value[i]
    except:
                log.warning('Could not initialize variables')
                FEWSConnect.logFileToXML(logFile, runInfo['outputDiagnosticFile'])
                sys.exit()
                
# Check if host site is available to retrieve MARFC files from sftp.

    port = int(port)
    try:
        # paramiko.util.log_to_file(tempDir + '\\paramiko.log')
        transport = Transport((host, port))
        transport.connect(username = usr, password = pw)
        sftp = SFTPClient.from_transport(transport)
        log.info('Succesfully connected to %s', host)
        print('Successfully connected to '+host)
    except:
        log.warning('Could not connect to %s', host)
        print('could not connect')
        print format_exc()


# defines number of hours (files) to retrieve based on lookback value (in days)
# This is defined very simply and assumes MARFC updates a new MPE file for every hour
# as was observed when this script was written.
    hrsback = int(lookback)*24
# Retrieve list of files from sftp site
    s=sftp.listdir(path)
# List of files in directory based on lookback period in hours
    allfiles=[filename for filename in s if filename.endswith('.gz')][-hrsback:]
#    print allfiles
#    exit ('test')

    for file in allfiles:
        grib = sftp.open(path+file,'rb').read()
#        Store file in FEWS import Directory
        with open(importDir +file, 'wb') as f:
            f.write(grib)
#        Store file in Archive Directory - TEMPORARILY SUSPEND
#        with open(archiveDir +file, 'wb') as a:
#            a.write(grib)

    # 6
    try:
        sftp.close()
        print("6 closed sftp object")
    except:
        print("6 sftp did not close")
    # 7
    try:
        f.close()#importDir.close()
        print("7 closed importDir object")
    except:
        print("7 importDir did not close")

    FEWSConnect.logFileToXML(logFile, runInfo['outputDiagnosticFile'])


