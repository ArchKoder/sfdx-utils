from subprocess import run
from datetime import datetime
from utilities import getManifestDir
from utilities import getLastModifiedFileName
from sfdxUtilitesConstants import FILE_TYPE_XML
from sfdxCommandFunctions import forceRetrieveDeploy
from utilities import getDefaultOrg

if __name__ == "__main__":
    username = input("enter org username/alias : ")
    if (username==''):
        username = getDefaultOrg()
    targetDir = getManifestDir()
    lastModifiedManifest = getLastModifiedFileName(targetDir,FILE_TYPE_XML)
    cmnd = forceRetrieveDeploy(username,targetDir+lastModifiedManifest)
    print(cmnd)
    run(cmnd,shell=True)
    print('retrieved '+lastModifiedManifest+' at '+datetime.now().strftime("%H:%M:%S"))