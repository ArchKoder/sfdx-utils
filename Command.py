from ObjectMap import ObjectMap
from subprocess import run

from sfdxUtilitesConstants import DUPLICATE_ARGUMENTS
from sfdxUtilitesConstants import ENTER_MANIFEST
from sfdxUtilitesConstants import ENTER_TARGETUSERNAME
from sfdxUtilitesConstants import FILE_TYPE_JSON
from sfdxUtilitesConstants import FILE_TYPE_XML
from sfdxUtilitesConstants import FORCE_ORG_DISPLAY
from sfdxUtilitesConstants import FORCE_SOURCE_DEPLOY
from sfdxUtilitesConstants import FORCE_SOURCE_RETRIEVE
from sfdxUtilitesConstants import JSON_OUTPUT
from sfdxUtilitesConstants import MANIFEST
from sfdxUtilitesConstants import TARGETUSERNAME

from utilities import getDefaultOrg
from utilities import getManifestDir
from utilities import getLastModifiedFileName
from utilities import combinePaths
class Argument:
    def __init__(this,name, **kwargs):
        this.name = name.lower()
        this.shortName = kwargs.get('shortName',None)
        this.shortName = this.shortName.lower() if this.shortName != None else ''
        this.inputStatement = kwargs.get('inputStatement',None)

    def __eq__(this, __o: object) -> bool:
        if (this.shortName == __o.shortName) or (this.name == __o.name):
            return True

    def __repr__(this) -> str:
        return '--'+this.name

    def askInput(this):
        if (this.inputStatement == None):
            return input('Enter '+this.name+' :\n')
        return input(this.inputStatement)



class Command:

    def __init__(this,name,optionalArguments,compulsoryArguments) -> None:
        this.optionalArguments = optionalArguments
        this.compulsoryArguments = compulsoryArguments
        this.valueMap = ObjectMap()
        this.initializeValueMap()
        this.name = name.lower()

    def initializeValueMap(this):
        for arg in this.optionalArguments:
            argValue = this.valueMap.get(arg,None)
            if(argValue != None):
                raise Exception(DUPLICATE_ARGUMENTS)
            else:
                this.valueMap.set(arg,None)


    def setArguments(this, arguments2ValueMap):
        for k,v in this.valueMap.items():
            this.valueMap.set(k,arguments2ValueMap.get(k,None))

    def getVerboseStatus(this):
        if(len(this.gerVerboseCommands) == 0):
            return False
        return True

    def gerVerboseCommands(this):
        verboseCommands = list()
        for argument in this.compulsoryArguments:
            if(this.valueMap.get(argument,None)==None):
                verboseCommands.append(argument)

        return verboseCommands


    def askVerboseInputs(this):
        for argument in this.gerVerboseCommands():
            this.valueMap.set(argument,argument.askInput())

    def getNonVerboseArguments(this):
        nonVerboseArguements = list()
        for argument in this.optionalArguments:
            if this.valueMap.get(argument,None) == None:
                nonVerboseArguements.append(argument)
        return nonVerboseArguements

    def populateNonVerboseArguments(this):
        nonVerboseArguments = this.getNonVerboseArguments()
        for argument in nonVerboseArguments:
            this.valueMap.set(argument,argument.populateNonVerboseInput())

    def generateCommandString(this):
        this.askVerboseInputs()
        this.populateNonVerboseArguments()

        cmnd = this.name
        for k,v in this.valueMap.items():
            k = ' '+k

            if isinstance(v,bool):
                if v:
                    cmnd += k
            else:
                value = ' "'+v+'"'
                cmnd += k+value

        return cmnd

    def run(this, **kwargs):
        shell = kwargs.get('shell',True)
        capture_output = kwargs.get('capture_output',False)
        if not capture_output:
            run(this.generateCommandString(),shell = shell, capture_output= capture_output)
        else:
            return run(this.generateCommandString(),shell = shell, capture_output= capture_output, text = True)

    
class Flag(Argument):
    def __init__(this, name, **kwargs):
        super().__init__(name, **kwargs)
        this.set = bool(kwargs.get('default',False))

    def askInput(this):
        this.populateNonVerboseInput()

    def populateNonVerboseInput(this):
        return this.set

jsonFlag = Flag(FILE_TYPE_JSON, default = True , inputStatement = JSON_OUTPUT)

manifestArg = Argument(MANIFEST, shortName = 'x', inputStatement = ENTER_MANIFEST)
def lastModifiedManifest():
    manifestDir = getManifestDir()
    latestManifestFile = getLastModifiedFileName(manifestDir,FILE_TYPE_XML)
    latestManifestFile = combinePaths([manifestDir,latestManifestFile])
    return str(latestManifestFile)
manifestArg.populateNonVerboseInput = lastModifiedManifest
targetusernameArg = Argument(TARGETUSERNAME,shortName = 'u',inputStatement=ENTER_TARGETUSERNAME)
targetusernameArg.populateNonVerboseInput = getDefaultOrg

orgDisplayCmnd = Command(FORCE_ORG_DISPLAY, [jsonFlag,targetusernameArg], [])
forceSourceDeployCmnd = Command(FORCE_SOURCE_DEPLOY, [jsonFlag,targetusernameArg,manifestArg],[])
forceSourceRetrieveCmnd = Command(FORCE_SOURCE_RETRIEVE, [jsonFlag,targetusernameArg,manifestArg],[])
