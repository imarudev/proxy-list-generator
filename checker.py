import requests
from requests.api import request
import sys
import urllib.request, socket

class Checker:
    def checkOne(self,ipport,sslverify=False,maxping = 1000):
        if len(ipport)>5:
            socket.setdefaulttimeout(30)

            try:        
                proxy_handler = urllib.request.ProxyHandler({'https': ipport})        
                opener = urllib.request.build_opener(proxy_handler)
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)        
                sock=urllib.request.urlopen('https://www.myip.com/')  # change the url address here
                return True
            except:        
                return False
            
    def checkMany(self,ipportlists,sslverify=False,maxping = 1000):
        results = []
        for ipport in ipportlists:
            proxy = {
                'http' : f'http://{str(ipport)}'
            }
            try:
                requests.get(url=self.urlforcheck,proxies=proxy,verify=sslverify,timeout=int(maxping/1000))
                results.append(ipport)
            except:
                return None

        return results
