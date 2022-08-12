from utilities import concatenateStrings
from sfdxUtilitesConstants import SFDX
from sfdxUtilitesConstants import FORCE_SOURCE_RETRIEVE
from sfdxUtilitesConstants import FORCE_SOURCE_DEPLOY
from sfdxUtilitesConstants import FORCE_APEX_EXECUTE
from sfdxUtilitesConstants import MANIFEST
from sfdxUtilitesConstants import TARGETUSERNAME
from sfdxUtilitesConstants import APEX_CODE_FILE

def forceSourceDeploy(targetUsername,manifest):
    cmndStrings = [SFDX,FORCE_SOURCE_DEPLOY,TARGETUSERNAME,targetUsername,MANIFEST,manifest]
    cmnd = concatenateStrings(cmndStrings,[3,5])
    return cmnd

def forceSourceRetrieve(targetUsername,manifest):
    cmndStrings = [SFDX,FORCE_SOURCE_RETRIEVE,TARGETUSERNAME,targetUsername,MANIFEST,manifest]
    cmnd = concatenateStrings(cmndStrings,[3,5])
    return cmnd

def forceApexExecute(targetUsername,apexScript):
    cmndStrings =[SFDX,FORCE_APEX_EXECUTE,TARGETUSERNAME,targetUsername,APEX_CODE_FILE,apexScript]
    cmnd = concatenateStrings(cmndStrings,[3,5])
    return cmnd
