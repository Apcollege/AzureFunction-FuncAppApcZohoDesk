'''
Created by Felipe Waltrick Pedro
ssh server: https://funcappapcaplication.scm.azurewebsites.net/webssh/host
api ZohoDesk: https://api-console.zoho.com.au/
doc api ZohoDesk: https://desk.zoho.com/DeskAPIDocument
http azure: https://docs.microsoft.com/en-us/python/api/azure-functions/azure.functions.httpresponse?view=azure-python
'''

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    from ZohoDeskOpenTicketV2.ZohoDesk import config
    from configparser import ConfigParser
    import ZohoDeskOpenTicketV2.ZohoDesk.function as func_generic
    import ZohoDeskOpenTicketV2.ZohoDesk.Authentication.authentication as token
    import ZohoDeskOpenTicketV2.ZohoDesk as ZohoDesk

    #Set config Info
    project_folder = config.config_object["GENERALCONFIG"]["temp_folder"] + "/ZohoDesk"
    config_object = ConfigParser()
    config_object.read(project_folder + "/config.ini")
    apiinfo = config_object["APICONFIG"]
    url_data = apiinfo["url_data"]

    #Get Body
    body = req.get_body()

    #Set URL Header Info
    email = req.headers.get('email')
    channel = req.headers.get('channel')
    subject = req.headers.get('subject')
    departmentId = req.headers.get('departmentId')
    status = req.headers.get('status')
    classification = req.headers.get('classification')
    assigneeId = req.headers.get('assigneeId')
    cf_unit = req.headers.get('cf_unit')
    priority = req.headers.get('priority')
    description = body.decode('utf-8').replace('"',"")

    #Get ZohoDesk Token
    tokenFirst  = str(token.getValidToken(1))

    #Get Id Contact ZohoDesk
    requestGetIdUserZohoDesk=func_generic.convert(func_generic.getIdUserZohoDesk(url_data, tokenFirst, email))
    idUserZohoDesk = requestGetIdUserZohoDesk['id']

    dataTicketInsert={
            "contactId" : idUserZohoDesk,
            "subject" : subject,
            "channel" : channel,
            "departmentId" : departmentId,
            "status" : status,
            "classification" : classification,
            "email" : email,
            "assigneeId" : assigneeId ,
            "description" : description,
            "priority" : priority,
            "cf" : {
               "cf_unit" : cf_unit
            }
        }

    #Create Ticket on ZohoDesk
    requestResultTicket = func_generic.createTicketZohoDesk(url_data, tokenFirst, dataTicketInsert)

    #return func.HttpResponse(f"{requestResultTicket}")
    return func.HttpResponse(status_code=requestResultTicket[0], body=requestResultTicket[1]) 