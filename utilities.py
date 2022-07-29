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
from sfdxUtilitesConstants import MANIFEST_MEMBERS
from sfdxUtilitesConstants import MANIFEST_NAME
from sfdxUtilitesConstants import SFDX_CONFIG_JSON_DEFAULTUSERNAME

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
            return sfdxConfigJson[SFDX_CONFIG_JSON_DEFAULTUSERNAME]

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

def mergeManifestDicts(manifestA,manifestB):
    """Return the dictionary after merging input ones."""
    #assume manifestB is shorter and then correct
    if(len(manifestA.keys())<len(manifestB.keys())):
        manifestA,manifestB = manifestB,manifestA
    
    for key in manifestB.keys():
        membersB = manifestB[key]
        membersA = manifestA.get(key,set())
        membersA = membersA.union(membersB)
        manifestA[key]=membersA
    
    return manifestA


def manifestToDict(targetDir,filename):
    finalManifest,memberSet = {},set()
    with open(targetDir+filename, 'r') as manifest:
        manifestContent = manifest.readlines()
        for line in manifestContent:
            if MANIFEST_MEMBERS in line:
                memberSet.add(line.strip())
            if MANIFEST_NAME in line:
                currentManifest = {}
                currentManifest[line.strip()]=memberSet
                finalManifest = mergeManifestDicts(finalManifest,currentManifest)
                memberSet=set()

    return finalManifest


def mergeManifests(filenames,targetDir,finalFileName=None):
    if(finalFileName==None):
        finalFileName=filenames[0]

    if(len(filenames)>0):
        finalManifest,memberSet = {},set()
        for filename in filenames:
            currentManifest= manifestToDict(targetDir,filename)
            finalManifest = mergeManifestDicts(finalManifest,currentManifest)

        dictToManifest(finalManifest,finalFileName,targetDir)