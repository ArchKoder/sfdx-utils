from os.path import getmtime as lastModifiedTime
from os import listdir as listDir
from os import getcwd
from json import load
from sfdxUtilitesConstants import FILE_TYPE_XML, MANIFEST_XML
from sfdxUtilitesConstants import MANIFEST_PACKAGE
from sfdxUtilitesConstants import MANIFEST_PACKAGE_CLOSE
from sfdxUtilitesConstants import MANIFEST_TYPES
from sfdxUtilitesConstants import MANIFEST_TYPES_CLOSE
from sfdxUtilitesConstants import MANIFEST_API_VERSION_53

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

def writeFile(fileLines,filename,targetDir,fileType,mode='a'):
    with open(targetDir+filename+'.'+fileType,mode) as file:
        file.writelines(line+'\n' for line in fileLines)


def dictToManifest(manifestDict,filename,targetDir):
    manifestLines = []
    manifestLines.append(MANIFEST_XML)
    manifestLines.append(MANIFEST_PACKAGE)

    for name in manifestDict.keys():
        manifestLines.append('\t'+MANIFEST_TYPES)

        for member in manifestDict[name]:
            manifestLines.append('\t\t'+member)
        
        manifestLines.append('\t\t'+name)
        manifestLines.append('\t'+MANIFEST_TYPES_CLOSE)

    manifestLines.append(MANIFEST_API_VERSION_53)
    manifestLines.append(MANIFEST_PACKAGE_CLOSE)

    writeFile(manifestLines,filename,targetDir,FILE_TYPE_XML,'w')


def mergeManifests(filenames,targetDir,finalFileName=None):
    if(finalFileName==None):
        finalFileName=filenames[0]

    if(len(filenames)>0):
        finalManifest,memberSet = {},set()

        for filename in filenames:
            filename = targetDir+filename
            with open(filename,'r') as currentManifest:
                manifestContent = currentManifest.readlines()
                for line in manifestContent:
                    if '<members>' in line:
                        memberSet.add(line.strip())
                    if '<name>' in line:
                        currentNameMembers = finalManifest.get(line.strip(),set())
                        currentNameMembers = currentNameMembers.union(memberSet)
                        finalManifest[line.strip()]=currentNameMembers
                        memberSet=set()
            
        print(finalManifest)
        dictToManifest(finalManifest,finalFileName,targetDir)