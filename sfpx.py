from sfdxUtilitesConstants import FILE_TYPE_XML
from sfdxUtilitesConstants import FILE_TYPE_JSON
from sfdxUtilitesConstants import OBJECT_API_NAME

from utilities import getLastModifiedFileName
from utilities import getManifestDir
from utilities import getDefaultOrg

from sfdxCommandFunctions import forceSourceRetrieve

from subprocess import run
from os import access, getcwd
from argparse import ArgumentParser
from os.path import exists
from json import load
from json import loads

from Command import jsonFlag
from Command import targetusernameArg
from Command import orgDisplayCmnd
from Command import forceSourceDeployCmnd
from Command import forceSourceRetrieveCmnd
class SFPXController:
    def __init__(this,projectDir,args) -> None:
        this.projectDir = projectDir
        this.args = args

    def deployManifest(this):
        forceSourceDeployCmnd.setArguments(args)
        forceSourceDeployCmnd.run()

    def retrieveManifest(this):
        forceSourceRetrieveCmnd.setArguments(args)
        forceSourceRetrieveCmnd.run()

    def bulkInsert(this):
        def getAccessToken(orgInformation):
            output = orgInformation.stdout
            output = loads(output).get('result')
            accessToken = output.get('accessToken')
            return accessToken

        accessToken = getAccessToken(this.displayOrg())
        print(accessToken)

    def displayOrg(this):
        orgDisplayCmnd.setArguments(args)
        orgInformation = orgDisplayCmnd.run(capture_output = True, shell = True)
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