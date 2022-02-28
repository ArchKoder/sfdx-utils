from subprocess import run
from os import getcwd
from os.path import getmtime as lastModifiedTime
from os import listdir as listDir
from os.path import isfile as isFile
from datetime import datetime

def getLastModifiedFileName(targetDir):
    def isXMLFile(f):
        if isFile(targetDir+f):
            if f.endswith('.xml'):
                return True
        return False

    files = [(f, lastModifiedTime(targetDir+f)) for f in listDir(targetDir) if isXMLFile(f)]
    files = sorted(files, key=lambda x: x[1], reverse=True)
    return files[0][0]

if __name__ == "__main__":
    #wd,manifestDir= 'getcwd()' , '/manifest/'
    wd,manifestDir= '.' , '/manifest/'
    #projectName = wd[wd.rfind('/')+1:]
    username = input("enter org username/alias : ")
    targetDir = wd+manifestDir
    lastModifiedManifest = getLastModifiedFileName(targetDir)
    cmnd = 'sfdx force:source:deploy'
    cmnd += ' -u '+username
    cmnd += ' -x '+targetDir+lastModifiedManifest
    print(cmnd)
    run(cmnd,shell=True)
    print('deployed '+lastModifiedManifest+' at '+datetime.now().strftime("%H:%M:%S"))