from os.path import getmtime as lastModifiedTime
from os import listdir as listDir
from os.path import isfile as isFile

def isFileTypeCorrect(fileName,fileType):
    try:
        if(fileName.endswith(fileType)):
            return True
        return False
    except:
        return False

def getLastModifiedFileName(targetDir,fileType):

    lastModifiedFileName = None
    tempLastModifiedTime = float('-inf')
    for fileName in listDir(targetDir):
        if isFileTypeCorrect(fileName,fileType):
            fileLastModifiedTime = lastModifiedTime(targetDir+'/'+fileName)
            if fileLastModifiedTime > tempLastModifiedTime:
                tempLastModifiedTime = fileLastModifiedTime
                lastModifiedFileName = fileName 
    return lastModifiedFileName
