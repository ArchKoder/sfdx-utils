from lib2to3.pgen2.grammar import opmap_raw
from sfdxUtilitesConstants import ORG_USERNAME_ALIAS
from sfdxUtilitesConstants import FILE_TYPE_XML
from utilities import getLastModifiedFileName
from utilities import getManifestDir
from utilities import getDefaultOrg
from utilities import validPath
from sfdxCommandFunctions import forceSourceDeploy
from sfdxCommandFunctions import forceSourceRetrieve
from subprocess import run
from os import getcwd
import sys
from argparse import ArgumentParser
class SFPXController:
    def __init__(this,projectDir) -> None:
        this.projectDir = projectDir

    def deployManifest(this,verbose=False):
        if(verbose):
            username = input(ORG_USERNAME_ALIAS)
        else:
            username = getDefaultOrg(this.projectDir)
        print(username)
        targetDir = getManifestDir(this.projectDir)
        print(targetDir)
        lastModifiedManifest = getLastModifiedFileName(targetDir,FILE_TYPE_XML)
        cmnd = forceSourceDeploy(username,targetDir+lastModifiedManifest)
        run(cmnd,shell=True)

    def retrieveManifest(this,verbose=False):
        if(verbose):
            username = input(ORG_USERNAME_ALIAS)
        else:
            username = getDefaultOrg(this.projectDir)
        targetDir = getManifestDir(this.projectDir)
        lastModifiedManifest = getLastModifiedFileName(targetDir,FILE_TYPE_XML)
        cmnd = forceSourceRetrieve(username,targetDir+lastModifiedManifest)
        run(cmnd,shell=True)

if __name__ == "__main__":
    cli = ArgumentParser()
    cli.add_argument("operation",help="base sfdx operation to be invoked")
    cli.add_argument("-v","--verbose",help="specifying it runs operation in verbose mode",action="store_true")
    cli.add_argument("-p","--projectDir", help = "specify path to sfdx project instead of current working directory")
    args = cli.parse_args()
    if(args.projectDir == None):
        args.projectDir = getcwd()
    try:
        sfpxController = SFPXController(args.projectDir)
    except:
        raise Exception('Invalid path for sfdx operation')
    operationToFunctionMap={
        'deploy':sfpxController.deployManifest,
        'retrieve':sfpxController.retrieveManifest
    }

    operation = operationToFunctionMap[args.operation]
    operation(args.verbose)