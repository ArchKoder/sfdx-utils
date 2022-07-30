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
    filenameList = fileSelector(getManifestDir(),FILE_TYPE_XML,searchTerm)
    finalManifestName = input("Enter desired name of the merged manifest:\n")
    mergeManifests(filenameList,getManifestDir(),finalManifestName)
    