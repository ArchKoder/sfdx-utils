from os.path import getmtime as lastModifiedTime
from os import listdir as listDir
from os.path import isfile as isFile
from os import getcwd
from json import load

def isFileTypeCorrect(fileName,fileType):
    try:
        if(fileName.endswith(fileType)):
            return True
        return False
    except:
        return False

def getLastModifiedFileName(targetDir,fileType=''):

    lastModifiedFileName = None
    tempLastModifiedTime = float('-inf')
    for fileName in listDir(targetDir):
        if isFileTypeCorrect(fileName,fileType):
            fileLastModifiedTime = lastModifiedTime(targetDir+'/'+fileName)
            if fileLastModifiedTime > tempLastModifiedTime:
                tempLastModifiedTime = fileLastModifiedTime
                lastModifiedFileName = fileName 
    return lastModifiedFileName

def getManifestDir():
    return getcwd() +'/manifest/'

def getDefaultOrg():
    try:
        with open('./.sfdx/sfdx-config.json') as sfdxConfig:
            sfdxConfigJson = load(sfdxConfig)
            return sfdxConfigJson['defaultusername']

    except:
        return ''

def mergeManifests(filenames,targetDir=None,finalFileName=None):
    if(finalFileName==None):
        finalFileName=filenames[0]

    for filename in filenames:
        filename = targetDir+filename
        with open(filename,'r') as currentManifest:
            manifestContent = currentManifest.read()
            for line in manifestContent:
                if '<types>' in line:
                    pass