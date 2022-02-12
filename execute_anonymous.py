from subprocess import run
from os import getcwd
from os.path import getmtime as lastModifiedTime
from os import listdir as listDir
from os.path import isfile as isFile
from datetime import datetime

def getLastModifiedFileName(targetDir):
    def isApexFile(f):
        if isFile(targetDir+f):
            if f.endswith('.apex'):
                return True
        return False

    files = [(f, lastModifiedTime(targetDir+f)) for f in listDir(targetDir) if isApexFile(f)]
    files = sorted(files, key=lambda x: x[1], reverse=True)
    return files[0][0]

if __name__ == "__main__":
    wd,scriptDir= getcwd() , '/scripts/apex/'
    projectName = wd[wd.rfind('/')+1:]
    targetDir = wd+scriptDir
    lastModifiedScript = getLastModifiedFileName(targetDir)
    cmnd = 'sfdx force:apex:execute '
    cmnd += '-u '+projectName+'.com '
    cmnd += '-f '+targetDir+lastModifiedScript
    cmnd += ' --json'
    print(cmnd)
    run(cmnd,shell=True)
    print('ran '+lastModifiedScript+' at '+datetime.now().strftime("%H:%M:%S"))
