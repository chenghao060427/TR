import requests,time
class getPorxyFail(Exception):
    def __str__(self):return '无法获取代理ip'
class proxy:
    __instans = None
    def __new__(cls, *args, **kwargs):
        if(cls.__instans is None):
            cls.__instans = super().__new__(cls)
            return cls.__instans
        else:
            return cls.__instans

    def __init__(self,proxy_url='',timeout=4*3600):
        self.proxy_url = proxy_url
        # self.proxy_url = proxy_url
        self.ips=[]
        self.get_ips_time=0
        self.timeout=timeout
    #获取ip
    def get_ips(self,num=1):
        if(int(time.time())-self.get_ips_time>self.timeout):
            self.reflesh_ips(num)
        return self.ips
    #刷新ips
    def reflesh_ips(self,num):
        self.get_ips_time = int(time.time())
        result = requests.get(url=self.proxy_url.format(num))
        if(result.status_code==200):
            self.ips=result.text.strip().split('\r\n')
        else:
            raise getPorxyFail()
        pass

if __name__ == "__main__":
    p = proxy('http://104.160.21.98:9049/v1/ips?num={}&country=US&state=newyork&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=')
    print(p.get_ips(2))
#http://104.160.21.98:9049/v1/ips?num=1&country=US&state=newyork&city=all&zip=all&t=txt&port=40000&isp=all&start=&end=