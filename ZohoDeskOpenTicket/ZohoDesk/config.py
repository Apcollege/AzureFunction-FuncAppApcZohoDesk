from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

config_object["USERINFO"] = {
    "user": "robot@apcollege.edu.au",
    "key": "Apcauto2021$$"
}

config_object["APICONFIG"] = {
    "client_id": "1000.BCHXWJI2VWHO4MLG23ZWZ151WTNYMC",
    "secret_id": "87e45a3788119f51c16dd1022a5791bd39ea913914",
    "redirect_uri": "https://localhost:5000",
    "scope": "Desk.tickets.CREATE,Desk.search.READ,Desk.settings.READ,Desk.basic.READ,Desk.tasks.ALL,Desk.contacts.READ,Desk.contacts.WRITE,Desk.contacts.UPDATE,Desk.contacts.CREATE,Desk.contacts.DELETE,Desk.settings.UPDATE",
    "url_auth": "https://accounts.zoho.com.au/oauth/v2",
    "url_data": "https://desk.zoho.com.au/api/v1"
}

import os
config_object["GENERALCONFIG"] = {
    "project_folder": os.getcwd()+'/ZohoDeskGetIdUser',
    "temp_folder":"/home/data/Functions"
}

def save_file_ini():
    #Write the above sections to config.ini file
    path_tmp=config_object["GENERALCONFIG"]["temp_folder"]+'/ZohoDesk'
    if not os.path.exists(path_tmp):
        os.makedirs(path_tmp)

    file = path_tmp+'/config.ini'
    with open(file, 'w') as conf:
        config_object.write(conf)
        
    return file

save_file_ini()