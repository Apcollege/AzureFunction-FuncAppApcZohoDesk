def convert(obj):
    if isinstance(obj, bool):
        return str(obj).lower()
    if obj == None:
        return str(obj)
    if isinstance(obj, (list, tuple)):
        return [convert(item) for item in obj]
    if isinstance(obj, dict):
        return {convert(key):convert(value) for key, value in obj.items()}
    return obj


def getIdUserZohoDesk(url_data, tokenFirst, email):
    try:
        import requests
        import json
        url = url_data + '/contacts/search'
        h = {"Authorization": "Zoho-oauthtoken " + tokenFirst}
        p = {"limit": 1, "email": email}
        requestResult = requests.get(url, headers=h, params=p).json()
        requestResultJson = requestResult["data"][0]
        return requestResultJson
    except:
        return "Not found"


def createTicketZohoDesk(url_data, tokenFirst, dataTicketInsert):
    import requests
    import json
    url = url_data + '/tickets'
    h = {"Authorization": "Zoho-oauthtoken " + tokenFirst}
    d = json.dumps(dataTicketInsert, indent = 4)
    d = d.replace("None","Null")
    requestResult = requests.post(url, headers=h, data=d)
    return requestResult.status_code, requestResult.text