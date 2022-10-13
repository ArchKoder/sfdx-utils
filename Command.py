from sfdxUtilitesConstants import DUPLICATE_ARGUMENTS
from ObjectMap import ObjectMap
from subprocess import run

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
        for k,v in arguments2ValueMap:
            if v != None:
                this.valueMap.set(k,v)
            else:
                this.valueMap.pop(k)

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
        for argument in this.getNonVerboseArguments():
            this.valueMap.set(argument,argument.askInput())

    def getNonVerboseArguments(this):
        nonVerboseArguements = list()
        for argument in this.optionalArguments:
            if this.valueMap.get(argument,None) == None:
                nonVerboseArguements.append(argument)
        print(nonVerboseArguements)
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
            value = ' "'+v+'"'
            cmnd += ' '+k+value
        return cmnd

    def run(this,shell = True):
        run(this.generateCommandString(),shell)

    
class Flag(Argument):
    def __init__(this, name, **kwargs):
        super().__init__(name, **kwargs)
        this.set = bool(kwargs.get('default',False))


targetUsernameArg = Argument('targetusername',shortName = 'u',inputStatement='A username or alias for the target org. Overrides the default target org.')
manifestArg = Argument('manifest',shortName = 'x',inputStatement = 'file that specifies the components to deploy')

deployCommand = Command('sfdx force:source:deploy',[targetUsernameArg],[manifestArg])
deployCommand.valueMap.set(manifestArg,'manifest/asdf.xml')
deployCommand.valueMap.set(targetUsernameArg,'15Sep')

print(deployCommand.generateCommandString())
