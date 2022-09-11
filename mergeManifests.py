from subprocess import run
from datetime import datetime
from utilities import getManifestDir
from sfdxUtilitesConstants import FILE_TYPE_XML
from utilities import fileSelector
from utilities import mergeManifests

if __name__ == "__main__":
    searchTerm = input('Enter search term for the manifests to merge:')
    if searchTerm =='':
        searchTerm=None
    indexToFileName,fileIndexList = fileSelector(getManifestDir(),FILE_TYPE_XML,searchTerm,True,'Enter space seperated indexes for manifests to merge')
    filenameList=[]
    for index in indexToFileName.keys():
        if (index in fileIndexList):
            filenameList.append(indexToFileName[index])
    indexToFileName,fileInputList = fileSelector(getManifestDir(),FILE_TYPE_XML,'',False,'Enter the file Index or new name for target manfest')

    if fileInputList[0] in indexToFileName.keys():
        finalManifestName = indexToFileName[fileInputList[0]]
    else:
        finalManifestName = fileInputList[0]

    mergeManifests(filenameList,getManifestDir(),finalManifestName)