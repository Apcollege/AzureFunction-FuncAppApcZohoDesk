import requests
import ZohoDeskOpenTicket.ZohoDesk.Authentication.autorization as autorizationZohoDesk
import os
from configparser import ConfigParser
import ZohoDeskOpenTicket.ZohoDesk.config as config

project_folder = config.config_object["GENERALCONFIG"]["project_folder"]+"/ZohoDesk"
path_tmp = config.config_object["GENERALCONFIG"]["temp_folder"]+'/ZohoDesk'


config_object = ConfigParser()
config_object.read(path_tmp+"/config.ini")
apiconfig = config_object["APICONFIG"]
generalconfig = config_object["GENERALCONFIG"]


def updateCurrentToken(request):
    token_object_updated = ConfigParser()
    token_object_updated["APITOKEN"]=request.json()
    apitoken_updated = token_object_updated["APITOKEN"]

    try:
        with open(path_tmp+"/authZohoDeskCurrent.ini", 'w') as conf:
            token_object_updated.write(conf)

        token_updated = apitoken_updated["access_token"]
    except:
        token_updated = ""

    return token_updated


def isApiActive(token):
    url=apiconfig['url_data']+'/contacts/count'
    h = {"Authorization": "Zoho-oauthtoken " + token}
    p = {"viewId": 2047000000013688}

    try:
        if token == "":
            isApiActive=0
        else:
            request = requests.get(url, headers = h, params = p)

            if request.status_code == 401:
                isApiActive=0
            else:
                isApiActive=1
    except:
        isApiActive=0

    return isApiActive


def newToken():
    codeAuthorization = autorizationZohoDesk.getAuthorization()
    p = {"code": codeAuthorization, "grant_type": "authorization_code", "client_id": apiconfig["client_id"], "client_secret": apiconfig["secret_id"], "redirect_uri": apiconfig["redirect_uri"]}
    request = requests.post(apiconfig["url_auth"]+"/token", params = p)

    token_object = ConfigParser()
    token_object["APITOKEN"]=request.json()
    with open(path_tmp+"/authZohoDeskNew.ini", 'w') as conf:
        token_object.write(conf)

    if os.path.exists(path_tmp+"/authZohoDeskRefreshed.ini"):
        os.remove(path_tmp+
        "/authZohoDeskRefreshed.ini")

    #UpddateCurrent Token File
    token_updated = updateCurrentToken(request)
    isApiValid = isApiActive(token_updated)

    return isApiValid


def refreshToken():
    token_object = ConfigParser()
    token_object.read(path_tmp+"/authZohoDeskNew.ini")
    apitoken = token_object["APITOKEN"]
    p = {"refresh_token": apitoken["refresh_token"], "client_id": apiconfig["client_id"], "client_secret": apiconfig["secret_id"],
         "scope": apiconfig["scope"], "redirect_uri": apiconfig["redirect_uri"], "grant_type": "refresh_token"}
    request = requests.post(apiconfig["url_auth"]+"/token", params = p)

    token_object = ConfigParser()
    token_object["APITOKENREFRESH"]=request.json()

    with open(path_tmp+"/authZohoDeskRefreshed.ini", 'w') as conf:
        token_object.write(conf)

    #UpdateCurrent Token File
    token_updated = updateCurrentToken(request)
    isApiValid = isApiActive(token_updated)

    return isApiValid


def getCurrentToken():
    try:
        token_object_current = ConfigParser()
        token_object_current.read(path_tmp+"/authZohoDeskCurrent.ini")
        apitoken_current = token_object_current["APITOKEN"]
        token_current = apitoken_current["access_token"]
    except:
        token_current = ""
    return token_current


def getValidToken(refresh):

    if refresh == 1:
        refreshToken()
        token_current = getCurrentToken()
    else:
        token_current = getCurrentToken()

    if isApiActive(token_current) == 1:
        token_valid=token_current
    else:
        isValid=refreshToken()
        if isValid == 1:
            token_valid = getCurrentToken()
        else:
            isValid=newToken()
            if isValid == 1:
                token_valid = getCurrentToken()
            else:
                token_valid = "Invalid"

    return(token_valid)

