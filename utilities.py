from os.path import getmtime as lastModifiedTime
from os import listdir as listDir
from os import getcwd
from os import walk
from json import load
from turtle import left
from sfdxUtilitesConstants import FILE_TYPE_XML, MANIFEST_XML, FILE_TYPE_CSV,FILE_TYPE_XLSX
from sfdxUtilitesConstants import MANIFEST_PACKAGE
from sfdxUtilitesConstants import MANIFEST_PACKAGE_CLOSE
from sfdxUtilitesConstants import MANIFEST_TYPES
from sfdxUtilitesConstants import MANIFEST_TYPES_CLOSE
from sfdxUtilitesConstants import MANIFEST_API_VERSION_53
from sfdxUtilitesConstants import MANIFEST_MEMBERS
from sfdxUtilitesConstants import MANIFEST_NAME
from sfdxUtilitesConstants import SFDX_CONFIG_JSON_DEFAULTUSERNAME
from sfdxUtilitesConstants import INVALID_PATH
from sfdxUtilitesConstants import INVALID_FILE_FORMAT
from pandas import DataFrame
from pandas import read_csv as readCsv
from pandas import read_excel as readExcel
from os.path import exists
from pathlib import Path

def isFileTypeCorrect(filename,fileType):
    try:
        if(filename.endswith('.'+fileType)):
            return True
        return False
    except:
        return False

def concatenateStrings(stringList,escapeStringNumbers):
    concatenatedString = ""
    for stringOrder in range(len(stringList)):
        if stringOrder in escapeStringNumbers:
            concatenatedString += " '"+stringList[stringOrder]+"'"
        else:
            concatenatedString += " "+stringList[stringOrder]
    return concatenatedString

def getLastModifiedFileName(targetDir,fileType=''):

    lastModifiedFileName = None
    tempLastModifiedTime = float('-inf')
    for filename in listDir(targetDir):
        if isFileTypeCorrect(filename,fileType):
            fileLastModifiedTime = lastModifiedTime(targetDir+'/'+filename)
            if fileLastModifiedTime > tempLastModifiedTime:
                tempLastModifiedTime = fileLastModifiedTime
                lastModifiedFileName = filename 
    return lastModifiedFileName

def getManifestDir(projectDir = None):
    if(projectDir == None):
        projectDir = getcwd()
    return projectDir +'/manifest/'

def getApexScriptDir():
    return getcwd() +'/scripts/apex/'

def getDefaultOrg(projectDir = None):
    if(projectDir == None):
        projectDir = '.'

    try:
        with open(projectDir+'/.sfdx/sfdx-config.json') as sfdxConfig:
            sfdxConfigJson = load(sfdxConfig)
            return sfdxConfigJson[SFDX_CONFIG_JSON_DEFAULTUSERNAME]

    except:
        return ''

def writeFile(fileLines,filename,targetDir,fileType,mode='a'):
    if not isFileTypeCorrect(filename,fileType):
        filename = filename+'.'+fileType
    with open(targetDir+filename,mode) as file:
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


def mergeManifests(filenames,targetDir,finalFileName):
    if(finalFileName==None):
        finalFileName=filenames[0]

    if(len(filenames)>0):
        finalManifest= {}
        for filename in filenames:
            currentManifest= manifestToDict(targetDir,filename)
            finalManifest = mergeManifestDicts(finalManifest,currentManifest)

        dictToManifest(finalManifest,finalFileName,targetDir)

def fileSelector(targetDir,fileType,searchTerm,showFileTable,inputMessage):
    indexToFileName ,index, data= {},1,{'Left Index':[],'Left Name':[],'Right Index':[],'Right Name':[]}
    for root, dirs, filenames in walk(targetDir):
        for filename in filenames:
            if (searchTerm==None) or (searchTerm in filename):
                if isFileTypeCorrect(filename,fileType):
                    indexToFileName[index]=filename
                    if(index%2==1):
                        data['Left Index'].append(index)
                        data['Left Name'].append(filename)
                    else:
                        data['Right Index'].append(index)
                        data['Right Name'].append(filename)
                    index+=1

    if(index%2==0):
        data['Right Index'].append('')
        data['Right Name'].append('')

    if(showFileTable):
        dataView = DataFrame(data)
        print(dataView.to_string(index=False , justify=left))

    fileIndexList = input('\n'+inputMessage+'\n\n')
    fileIndexList = [safeIntegerConverter(index) for index in fileIndexList.split()]
    filenameList = []
    """
    for index in indexToFileName.keys():
        if (index in fileIndexList):
            filenameList.append(indexToFileName[index])
    """
    
    return (indexToFileName,fileIndexList)

def safeIntegerConverter(value):
    try:
        return int(value)
    except:
        return str(value)

def validateFilePaths(file):
    """checks if given path is a valid file Path"""
    try:
        filePath = Path(file)
        return filePath.is_file()
    except:
        return False


def fileFormat(file):
    """returns file format for given path."""
    if not validateFilePaths(file):
        raise Exception(INVALID_PATH)
    else:
        fileSplits = file.split('.')
        if(len(fileSplits)<2):
            raise Exception(INVALID_FILE_FORMAT)
        else:
            format = str(fileSplits[-1]).lower()
            return format

def pandasImportHelper(file):
    format2Importer = {
        FILE_TYPE_CSV : readCsv,
        FILE_TYPE_XLSX : readExcel
    }

    importer = format2Importer.get(fileFormat(file),None)
    if(importer == None):
        raise Exception(INVALID_FILE_FORMAT)
    else:
        return importer(file)


def assertFormat(file,formalFormat):
    actualFormat = fileFormat(file)
    if(actualFormat != formalFormat):
        raise Exception(INVALID_FILE_FORMAT)