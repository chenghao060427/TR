import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class browserException(Exception):
    def __init__(self,message=''):
        self.message=message
    def __str__(self):
        return self.message
class ads_browser:
    __instans = None
    def __new__(cls, *args, **kwargs):
        if(cls.__instans is None):
            cls.__instans = super().__new__(cls)
            return cls.__instans
        else:
            return cls.__instans
    def __init__(self):
        self.base_url= 'http://local.adspower.net:50325'
        pass
    #获取driver
    def get_driver(self,user_id):
        open_url = "http://local.adspower.net:50325/api/v1/browser/start?open_tabs=1&ip_tab=0&user_id={}&enable_password_saving=0&launch_args=[\"--disable-notifications\"]".format(user_id)

        resp = requests.get(open_url).json()
        print(resp)
        if resp["code"] != 0:
            raise browserException(resp["msg"])
        else:
            chrome_driver = resp["data"]["webdriver"]
            chrome_options = Options()
            # prefs = {"credentials_enable_service": False,
            #          "profile.password_manager_enabled": False
            #          }
            # chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
            driver = webdriver.Chrome(chrome_options,service=Service(chrome_driver))

            return driver
        pass
    #关闭浏览器
    def close_driver(self,user_id):
        close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + user_id
        requests.get(close_url)

    def create_account(self,account_infor):
        creat_url=self.base_url+'/api/v1/user/create'
        # print(creat_url)
        resp = requests.post(creat_url,json=account_infor).json()
        print(resp)
        if resp["code"] != 0:
            raise browserException(resp["msg"])
        else:
            return resp['data']['id']
        pass
    def update_account(self,account_infor):
        update_url= self.base_url+'/api/v1/user/update'
        resp = requests.post(update_url,json=account_infor).json()
        if resp["code"] != 0:
            raise False
        else:
            return True
        pass
    def del_account(self,user_infor):
        del_url = self.base_url+'/api/v1/user/delete'
        resp = requests.post(del_url,json=user_infor).json()
        if resp["code"] != 0:
            raise False
        else:
            return True
        pass

    def search_account(self,query):
        search_url = self.base_url+'/api/v1/user/list'
        resp = requests.get(search_url,params=query).json()
        if resp["code"] != 0:
            return []
        else:
            return resp['data']['list']
        pass

    def delete_cache(self):
        clear_url = self.base_url+'/api/v1/user/delete-cache'
        resp = requests.post(clear_url).json()
        if resp["code"] != 0:
            raise False
        else:
            return True
        pass
    def check_user(self,user_id):
        check_url = 'http://localhost:50325/api/v1/browser/active?user_id={}'.format(user_id)
        resp = requests.get(check_url).json()
        print(resp)
        pass
    def search_group(self,query):
        search_url = self.base_url+'/api/v1/group/list'
        resp = requests.get(search_url,params=query).json()
        if resp["code"] != 0:
            return []
        else:
            return resp['data']['list']
        pass
if __name__ == "__main__":
    a = ads_browser()
    group_list = a.search_account(query={'group_id':'3492708','page_size':100})
    print(group_list)
    # d = a.get_driver(user_id='jdbd88g')


