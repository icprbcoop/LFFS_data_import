#from urllib.request import urlopen
import urllib2
import datetime
import sys
import FEWSConnect
import logging
from suds.client import Client


FEWSServer = sys.argv[2]
WSDLLocation = 'FewsPiService?WSDL'

if (__name__ == '__main__'):
    # requested_dir is only needed for pulling a file froma directory
    # file location and name
    # requested_dir= r"C:\Users\Public\Documents\Python Scripts"
    # file_name = "\Test_CSV"
    file_name ="/coop_pot_withdrawals"
    # select file type
    extension = ".csv"
    # #assigns a datae and time to file
    date_time = str((datetime.datetime.now().strftime("_%Y%m%d_%H"))) #"here and now"
    # #opens requested file
    # requested_file = open(requested_dir + file_name + extension, "r+")
    #runInfoFile = sys.argv[1]
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
    
    


    requested_file = urllib2.urlopen('https://icprbcoop.org/drupal4/products/coop_pot_withdrawals.csv')

    #read requested file content to file_content
    file_content = requested_file.read()
    #where new file will be created
    destination = r"/home/user1/Documents"
    #creates new file
    new_file = open(destination + file_name + date_time + extension, "wb")
    #writes content of file_content to new_file
    new_file.write(file_content)
    new_file.close()
    requested_file.close()
    

#if __name__ == '__main__':
#    main()

