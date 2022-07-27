def forceSourceDeploy(targetUsername,manifest):
    cmnd = 'sfdx force:source:deploy'
    cmnd += ' --targetusername '+targetUsername
    cmnd += ' --manifest '+manifest
    return cmnd