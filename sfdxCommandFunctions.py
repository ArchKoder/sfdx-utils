def forceSourceDeploy(targetUsername,manifest):
    cmnd = 'sfdx force:source:deploy'
    cmnd += ' --targetusername '+targetUsername
    cmnd += ' --manifest '+manifest
    return cmnd

def forceSourceDeploy(targetUsername,manifest):
    cmnd = 'sfdx force:source:retrieve'
    cmnd += ' --targetusername '+targetUsername
    cmnd += ' --manifest '+manifest
    return cmnd