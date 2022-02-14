from bs4 import BeautifulSoup
import requests
from random import choice
from pathlib import Path


class UsProxyOrg:
    def getUseragent(self):
        self.pathtofile = Path("assets/useragents.txt")
        if self.pathtofile.is_file:
            with self.pathtofile.open(mode='r') as usragent:
                return choice(usragent.read().split('\n'))
        else:
            return None

    def __init__(self):
        self.header = {
            'User-Agent' : str(self.getUseragent())
        }
        self.url = 'https://www.us-proxy.org/'

    def getProxyLists(self):
        try:
            listresults=[]
            req = requests.get(url=self.url,headers=self.header,timeout=30)
            content = req.content
            soup = BeautifulSoup(content,'lxml')
            div = soup.find('div','table-responsive')
            tabel = div.find('table')
            tr = tabel.find_all('tr')
            for i in tr:
                tdnya = i.find_all('td')
                if len(tdnya) > 7:
                    dictresults = {}
                    dictresults['ipport'] = f'{tdnya[0].text.strip()}:{tdnya[1].text.strip()}'
                    dictresults['anonym'] = tdnya[4].text
                    dictresults['country'] = tdnya[3].text
                    dictresults['last_checked'] = tdnya[7].text
                    listresults.append(dictresults)
            return listresults
        except:
            return None
