from requests import post

from platformHelper import PlatformHelper
from sfdxUtilitesConstants import (ASSIGNMENT_RULE_ID, COLUMN_DELIMITER,
                                   CONTENT_TYPE, EXTERNAL_ID_FIELD_NAME,
                                   LINE_ENDING, OBJECT, OPERATION)


class BulkAPIHelper:

    def __init__(this,**kwargs):
        this.platformHelper = PlatformHelper()
        this.sessionId = kwargs.get('sessionId')
        this.domainName = kwargs.get('domainName')

    def createJob(this,**kwargs):
        def generateHeader():
            headers = {'Authorization': 'Bearer' + this.sessionId}
            return headers

        def generateURI():
            uri = 'http://'+this.domainName+'.my.salesforce.com/services/data/v50.0/jobs/ingest'
            return uri

        createRequestBody = {
            LINE_ENDING : this.platformHelper.lineEnding
        }

        for key,value in kwargs.items():
            if this.validateRequestProperty(key,value):
                createRequestBody[key] = value

        createResponse = post(generateURI(),data = createRequestBody,headers=generateHeader())
        return createResponse

        

    def validateRequestProperty(this,property,value):
        if property in [OPERATION,OBJECT]:
            if value == None:
                raise Exception(property+' is mandatory!')
            else:
                return True
        elif property in [ASSIGNMENT_RULE_ID,COLUMN_DELIMITER,CONTENT_TYPE,EXTERNAL_ID_FIELD_NAME]:
            if value != None:
                return True

        else:
            return False

    def getSessionId(this):
        pass
