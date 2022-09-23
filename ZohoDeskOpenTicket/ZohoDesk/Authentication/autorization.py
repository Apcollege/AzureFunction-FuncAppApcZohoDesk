#https://api-console.zoho.com.au/

from configparser import ConfigParser
import ZohoDeskOpenTicket.ZohoDesk.config as config

path_tmp = config.config_object["GENERALCONFIG"]["temp_folder"]+'/ZohoDesk'

#Read config.ini file
config_object = ConfigParser()
config_object.read(path_tmp+"/config.ini")

userinfo = config_object["USERINFO"]
user = userinfo["user"]
key = userinfo["key"]

apiconfig = config_object["APICONFIG"]
client_id = apiconfig["client_id"]
scope = apiconfig["scope"]
redirect_uri = apiconfig["redirect_uri"]
url_auth = apiconfig["url_auth"]

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getAuthorization():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec
    import time
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(ChromeDriverManager().install())
    authorisation_url=url_auth+"/auth?scope="+scope+"&client_id="+client_id+"&response_type=code&access_type=offline&redirect_uri="+redirect_uri+"&prompt=consent"

    driver.get(authorisation_url)

    driver.find_element_by_id("login_id").send_keys(user)
    driver.find_element(By.XPATH, '//*[@id="nextbtn"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(key)
    driver.find_element(By.XPATH, '//*[@id="nextbtn"]').click()
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, '//*[@id="user_details_container"]/button[1]').click()
    except:
        "Not find button Timezone"
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/a').click()
    except:
        "Not find button Limit Login"
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="Approve_Reject"]/button[1]').click()
    time.sleep(2)
    request_uri = driver.current_url
    driver.close()
    codeAuthorization = find_between(request_uri,'/?code=','&')
    return codeAuthorization
