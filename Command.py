from sfdxUtilitesConstants import DUPLICATE_ARGUMENTS
from ObjectMap import ObjectMap

class Argument:
    def __init__(this,name,shortName, **kwargs):
        this.name = name.lower()
        this.shortName = shortName.lower()
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
        this.optionalArguments = set(optionalArguments)
        this.compulsoryArguments = set(compulsoryArguments)
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
        verboseCommands = set()
        for argument in this.compulsoryArguments:
            if(this.valueMap.get(argument,None)==None):
                verboseCommands.add(argument)

        return verboseCommands


    def askVerboseInputs(this):
        for argument in this.getVerboseCommands():
            this.valueMap.set(argument,argument.askInput())

    def getNonVerboseArguments(this):
        nonVerboseArguements = set()
        for argument in this.optionalArguments:
            if this.valueMap.get(argument,None) == None:
                nonVerboseArguements.add(argument)
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
            cmnd += k+value
        return cmnd