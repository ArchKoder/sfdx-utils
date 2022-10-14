from sfdxUtilitesConstants import FILE_TYPE_XML
from sfdxUtilitesConstants import FILE_TYPE_JSON
from sfdxUtilitesConstants import OBJECT_API_NAME

from utilities import getLastModifiedFileName
from utilities import getManifestDir
from utilities import getDefaultOrg
from utilities import validateFilePaths
from utilities import assertFormat
from utilities import pandasImportHelper

from sfdxCommandFunctions import forceSourceDeploy
from sfdxCommandFunctions import forceSourceRetrieve

from subprocess import run
from os import getcwd
from argparse import ArgumentParser
from os.path import exists
from json import load

from Command import jsonFlag
from Command import targetusernameArg
from Command import orgDisplayCmnd
class SFPXController:
    def __init__(this,projectDir,args) -> None:
        this.projectDir = projectDir
        this.args = args

    def deployManifest(this,verbose=False):
        if(verbose):
            username = input('ORG_USERNAME_ALIAS')
        else:
            username = getDefaultOrg(this.projectDir)
        targetDir = getManifestDir(this.projectDir)
        lastModifiedManifest = getLastModifiedFileName(targetDir,FILE_TYPE_XML)
        cmnd = forceSourceDeploy(username,targetDir+lastModifiedManifest)
        run(cmnd,shell=True)

    def retrieveManifest(this,verbose=False):
        if(verbose):
            username = input('ORG_USERNAME_ALIAS')
        else:
            username = getDefaultOrg(this.projectDir)
        targetDir = getManifestDir(this.projectDir)
        lastModifiedManifest = getLastModifiedFileName(targetDir,FILE_TYPE_XML)
        cmnd = forceSourceRetrieve(username,targetDir+lastModifiedManifest)
        run(cmnd,shell=True)

    def bulkInsert(this):
        orgInformation = this.displayOrg()
        print(orgInformation)

    def displayOrg(this):
        orgDisplayCmnd.setArguments(args)
        orgInformation = orgDisplayCmnd.run(captureoutput = True, shell = True)
        return orgInformation


if __name__ == "__main__":
    cli = ArgumentParser()
    arguments = [targetusernameArg]
    commands = [orgDisplayCmnd]
    flags = [jsonFlag]

    cli.add_argument("operation",help="base sfdx operation to be invoked")

    for argument in arguments:
        cli.add_argument('-'+argument.shortName, str(argument), help= argument.inputStatement)

    for flag in flags:
        if flag.set == True:
            action = "store_true"
        else:
            action = "store_false"
        cli.add_argument('-'+flag.shortName, str(flag),action = action)

    args = vars(cli.parse_args())

    projectDir = getcwd()
    try:
        sfpxController = SFPXController(projectDir, args)
    except:
        raise Exception('Invalid path for sfdx operation')

    operation2FunctionMap={
        'deploy':sfpxController.deployManifest,
        'retrieve':sfpxController.retrieveManifest,
        'bulkInsert':sfpxController.bulkInsert,
        'displayOrg':sfpxController.displayOrg
    }
    operation = operation2FunctionMap[args['operation']]    
    operation()