from subprocess import run
from datetime import datetime
from utilities import getApexScriptDir
from utilities import getLastModifiedFileName
from sfdxUtilitesConstants import FILE_TYPE_APEX
from sfdxCommandFunctions import forceApexExecute
from utilities import getDefaultOrg

if __name__ == "__main__":
    username = input("enter org username/alias : ")
    if (username==''):
        username = getDefaultOrg()
    targetDir = getApexScriptDir()
    lastModifiedScript = getLastModifiedFileName(targetDir,FILE_TYPE_APEX)
    cmnd = forceApexExecute(username,targetDir+lastModifiedScript)
    print(cmnd)
    run(cmnd,shell=True)
    print('ran '+lastModifiedScript+' at '+datetime.now().strftime("%H:%M:%S"))
