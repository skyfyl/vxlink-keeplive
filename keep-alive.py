import requests
import logging
import schedule
import time

from configparser import ConfigParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run(user,pwd, keep_type, ids):
    logging.info("work type: {}".format(keep_type))
    session = requests.Session()
    response = session.get("https://vx.link/x2/login")
    token=''
    if response.status_code == 200:
        logging.info("get token success")
        cookies = response.cookies
        if cookies["PHPSESSID"]:
            token = cookies["PHPSESSID"]
        else:
            logging.error("get token err, status_code: %s, msg: %s" % (response.status_code, "not token sessid"))
    else:
        logging.error("get token err, status_code: %s, msg: %s" % (response.status_code, response.text))
    
    response = session.get("https://vx.link/openapi/v1/user?token={}&username={}&password={}&action=login".format(token,user,pwd))

    if response.status_code == 200:
        logging.info("login success")
    else:
        logging.error("login err, status_code: %s, msg: %s" % (response.status_code, response.text))
    
    for id in ids:
        response = session.get("https://vx.link/openapi/v1/vxtrans?action={}&token={}&id={}".format(keep_type, token, id))
        if response.status_code == 200:
            logging.info(response.url)            
        else:
            logging.error("keep alive err, status_code: %s, msg: %s" % (response.status_code, response.text))
        

if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('config.ini')
    user = cfg.get('login','user')
    pwd = cfg.get('login','pwd')
    ids = cfg.get('nodes','nodes_ids').split(',')
    on_time = str(cfg.get('time','keep_on_time'))
    off_time = str(cfg.get('time','keep_off_time'))
    # run("endysaiwang","a123456", "keep_off", ids)
    logging.info("start work, on time: {}, off time: {}".format(on_time, off_time))
    schedule.every().day.at(on_time).do(run, user= user,pwd=pwd, keep_type="keep_on", ids = ids)
    schedule.every().day.at(off_time).do(run, user= user,pwd=pwd, keep_type="keep_off", ids = ids)
    while True:
        schedule.run_pending()
        time.sleep(1)