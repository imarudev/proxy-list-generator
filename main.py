from os import close, stat
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import requests
from pathlib import Path
from random import choice
from bs4 import BeautifulSoup
from requests.sessions import session
from targetlistproxy import ipaddresscom,sslproxyorg,usproxyorg,socksproxynet,freeproxylistnet
from checker import Checker
from time import sleep


class ProxyApp:
    

    def cekproxy(self,listip,maxping):
        newobj = Checker()
        for ip in listip:
            while self.pausecheck:
                sleep(3)
            self.totaldicek+=1
            if len(ip) > 5:
                if newobj.checkOne(ipport=ip,maxping=maxping):
                    self.proxyaktif+=1
                    self.tkinterscrolledtext2.insert('end',f'{ip}\n')
                    self.label2.config(text=f'Proxy Active {self.proxyaktif}')
            self.label3.config(text=f'{self.totaldicek} Checked')
    def bukagetproxywindow(self):
        window = GetProxyLists()
        window.run()
    def handlecheck(self):
        
        getlist = self.tkinterscrolledtext1.get('1.0','end').split('\n')
        jumlahinput = len(getlist)
        self.label1.config(text=f"Proxy lists {jumlahinput}")
        if jumlahinput < 10:
            jumlahThread = 3
        elif jumlahinput < 20:
            jumlahThread = 5
        elif jumlahinput < 50:
            jumlahThread = 10
        elif jumlahinput < 100:
            jumlahThread = 20
        elif jumlahinput < 200:
            jumlahThread = 30
        else:
            jumlahThread = 50

        totalipperthread = int(len(getlist)/jumlahThread)
        Threadlist = []
        for d in range(jumlahThread):
            ifc = d+1
            if ifc == 1:
                dictip = getlist[:totalipperthread]
            elif ifc < jumlahThread:
                dictip = getlist[totalipperthread*d:totalipperthread*ifc]
            else:
                dictip = getlist[totalipperthread*d:]

            if self.entrytimeot.get() != '':
                if int(self.entrytimeot.get()) < 250:
                    maxtime = 250
                else:
                    maxtime = int(self.entrytimeot.get())
            else:
                maxtime = 1000
            Threadlist.append(threading.Thread(target=self.cekproxy,daemon=True,args=(dictip,maxtime,)))

        for startkuy in Threadlist:
            startkuy.start()
        for joinkuy in Threadlist:
            joinkuy.join()
        self.checkproxy.config(state=NORMAL,text="cek proxy",command=self.buttoncek)
        self.label3.config(text=f'{self.totaldicek} Checked\nSelesai')
    def cekresume(self):
        self.pausecheck = False
        self.checkproxy.config(text="Pause",command=self.cekpause)
    def cekpause(self):
        self.pausecheck = True
        self.checkproxy.config(text="Resume",command=self.cekresume)
    def buttoncek(self):
        self.pausecheck = False
        self.checkproxy.config(text="Pause",command=self.cekpause)
        self.button3.config(state=NORMAL)
        threading.Thread(target=self.handlecheck,daemon=True).start()
    def buttongetproxy(self):
        bukawindow = threading.Thread(target=self.bukagetproxywindow,daemon=True)
        bukawindow.start()
    def tangkaplists(self,listnya):
        self.tkinterscrolledtext1.insert('end',listnya.strip())
        total = len(listnya.strip().split('\n'))
        self.label1.config(text=f"Proxy lists {total}")
    def __init__(self, master=None):
        self.pausecheck = False
        self.totaldicek = 0
        self.proxyaktif = 0
        # build ui
        self.mainwindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame1 = tk.Frame(self.mainwindow)
        self.tkinterscrolledtext1 = ScrolledText(self.frame1)
        self.tkinterscrolledtext1.configure(background='#8ecae6', font='TkDefaultFont', height='10', state='normal')
        self.tkinterscrolledtext1.configure(width='25')
        self.tkinterscrolledtext1.grid(column='0', row='1')
        self.label1 = tk.Label(self.frame1)
        self.label1.configure(background='#023047', foreground='#ffffff', text='Proxy lists')
        self.label1.grid(column='0', row='0', sticky='nw')
        self.frame1.configure(background='#023047', height='200', width='200')
        self.frame1.grid(column='0', row='0')
        self.frame2 = tk.Frame(self.mainwindow)
        self.tkinterscrolledtext2 = ScrolledText(self.frame2)
        self.tkinterscrolledtext2.configure(background='#8ecae6', font='TkDefaultFont', height='10', state='normal')
        self.tkinterscrolledtext2.configure(width='25')
        self.tkinterscrolledtext2.grid(column='0', row='1')
        self.label2 = tk.Label(self.frame2)
        self.label2.configure(background='#023047', foreground='#ffffff', text='Proxy Active')
        self.label2.grid(column='0', row='0', sticky='nw')
        self.frame2.configure(background='#023047', height='200', width='200')
        self.frame2.grid(column='1', row='0')
        self.frame3 = tk.Frame(self.mainwindow)
        self.checkproxy = tk.Button(self.frame3)
        self.checkproxy.configure(activebackground='#8ecae6', background='#fb8500', font='system', height='1')
        self.checkproxy.configure(text='cek proxy', width='13',command=self.buttoncek)
        self.checkproxy.grid(column='0', pady='2', row='1')
        self.getproxy = tk.Button(self.frame3)
        self.getproxy.configure(activebackground='#ffb703', background='#219ebc', font='system', height='1')
        self.getproxy.configure(text='get proxy', width='13',command=self.buttongetproxy)
        self.getproxy.grid(column='0', pady='2', row='2')
        self.frame5 = tk.Frame(self.frame3)
        self.label5 = tk.Label(self.frame5)
        self.label5.configure(background='#023047', foreground='#ffffff', text='Timeout ms:')
        self.label5.pack(pady='2', side='left')
        self.entrytimeot = tk.Entry(self.frame5)
        def only_numbers(char):
            return char.isdigit()
        validation = self.mainwindow.register(only_numbers)
        self.entrytimeot.configure(background='#06d6a0', width='6',validate="key", validatecommand=(validation, '%S'))
        self.entrytimeot.pack(side='right')
        self.frame5.configure(background='#023047')
        self.frame5.grid(column='0', row='0')
        self.frame3.configure(background='#023047')
        self.frame3.grid(column='0', ipadx='1', row='1')
        self.frame4 = tk.Frame(self.mainwindow)
        self.button3 = tk.Button(self.frame4)
        self.button3.configure(state=DISABLED,activebackground='#ffb703', background='#219ebc', font='system', text='Copy Lists')
        self.button3.pack(side='top')
        self.label3 = ttk.Label(self.frame4)
        self.label3.configure(background='#023047', font='system', foreground='#ffd166', justify='center')
        self.label3.configure(text='Ready...')
        self.label3.pack(anchor='center', fill='both', ipadx='15', ipady='5', pady='3', side='bottom')
        self.frame4.configure(background='#023047', height='200', width='200')
        self.frame4.grid(column='1', ipadx='25', row='1')
        self.mainwindow.configure(background='#023047', height='200', width='200')
        self.mainwindow.title('Proxy Tools')

        # Main widget
        self.mainwindow = self.mainwindow
    
    def run(self):
        self.mainwindow.mainloop()

class GetProxyLists:
    def handlegetproxy(self,target):
        'list of target! 1=free-proxy-list.net, 2=ip-address.com, 3=sslproxy.org, 4=socks-proxy.net, 5=us-proxy.org'
        if target == 1:
            self.loggeproxytproses.config(text="Getting proxy lists from : free-proxy-list.net")
            getarget = freeproxylistnet.FreeProxyListNet()
            listsdict = getarget.getProxyLists()
            if listsdict != None:
                count = 0
                for ld in listsdict:
                    count+=1
                    ip = ld['ipport']
                    self.tkinterscrolledtext4.insert('end',f'{ip}\n')
                self.loggeproxytproses.config(text=f"Getting done with {count} results")
            else:
                self.loggeproxytproses.config(text="Getting error...")
            self.button20.config(state=NORMAL)
        elif target == 2:
            self.loggeproxytproses.config(text="Getting proxy lists from : ip-address.com")
            getarget = ipaddresscom.IpAddressCom()
            listsdict = getarget.getProxyLists()
            if listsdict != None:
                count = 0
                for ld in listsdict:
                    count+=1
                    ip = ld['ipport']
                    self.tkinterscrolledtext4.insert('end',f'{ip}\n')
                self.loggeproxytproses.config(text=f"Getting done with {count} results")
            else:
                self.loggeproxytproses.config(text="Getting error...")
            self.button9.config(state=NORMAL)
        elif target == 3:
            self.loggeproxytproses.config(text="Getting proxy lists from : sslproxies.org")
            getarget = sslproxyorg.SslProxyOrg()
            listsdict = getarget.getProxyLists()
            if listsdict != None:
                count = 0
                for ld in listsdict:
                    count+=1
                    ip = ld['ipport']
                    self.tkinterscrolledtext4.insert('end',f'{ip}\n')
                self.loggeproxytproses.config(text=f"Getting done with {count} results")
            else:
                self.loggeproxytproses.config(text="Getting error...")
            self.button17.config(state=NORMAL)
        elif target == 4:
            self.loggeproxytproses.config(text="Getting proxy lists from : socks-proxy.net")
            getarget = socksproxynet.SocksProxyNet()
            listsdict = getarget.getProxyLists()
            if listsdict != None:
                count = 0
                for ld in listsdict:
                    count+=1
                    ip = ld['ipport']
                    self.tkinterscrolledtext4.insert('end',f'{ip}\n')
                self.loggeproxytproses.config(text=f"Getting done with {count} results")
            else:
                self.loggeproxytproses.config(text="Getting error...")
            self.button16.config(state=NORMAL)
        elif target == 5:
            self.loggeproxytproses.config(text="Getting proxy lists from : us-proxy.org")
            getarget = usproxyorg.UsProxyOrg()
            listsdict = getarget.getProxyLists()
            if listsdict != None:
                count = 0
                for ld in listsdict:
                    count+=1
                    ip = ld['ipport']
                    self.tkinterscrolledtext4.insert('end',f'{ip}\n')
                self.loggeproxytproses.config(text=f"Getting done with {count} results")
            else:
                self.loggeproxytproses.config(text="Getting error...")
            self.button18.config(state=NORMAL)
        else:
            pass
        totalresult = len(self.tkinterscrolledtext4.get('1.0','end').strip().split('\n'))
        self.label4.config(text=f'Proxy results {totalresult}')

    def buttonfreproxylisnet(self):
        self.button20.config(state=DISABLED)
        threading.Thread(target=self.handlegetproxy,daemon=True,args=(1,)).start()
    def buttonipaddresscom(self):
        self.button9.config(state=DISABLED)
        threading.Thread(target=self.handlegetproxy,daemon=True,args=(2,)).start()
    def buttonsocksproxynet(self):
        self.button17.config(state=DISABLED)
        threading.Thread(target=self.handlegetproxy,daemon=True,args=(3,)).start()
    def buttonsslproxyorg(self):
        self.button16.config(state=DISABLED)
        threading.Thread(target=self.handlegetproxy,daemon=True,args=(4,)).start()
    def buttonusproxyorg(self):
        self.button18.config(state=DISABLED)
        threading.Thread(target=self.handlegetproxy,daemon=True,args=(5,)).start()

    def inserttolists(self):
        getlist = self.tkinterscrolledtext4.get('1.0','end')
        insertolist(getlist)
        messagebox.showinfo(title="inserted",message="Successfully inserted")
        self.getProxyWindow.destroy()
        

    def __init__(self, master=None):
        # build ui
        self.getProxyWindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame9 = tk.Frame(self.getProxyWindow)
        self.frame14 = tk.Frame(self.frame9)
        self.tkinterscrolledtext4 = ScrolledText(self.frame14)
        self.tkinterscrolledtext4.configure(background='#8ecae6', font='TkDefaultFont', height='10', state='normal')
        self.tkinterscrolledtext4.configure(width='25')
        self.tkinterscrolledtext4.grid(column='0', row='1')
        self.label4 = tk.Label(self.frame14)
        self.label4.configure(background='#606c38', foreground='#fefefe', text='Proxy results')
        self.label4.grid(column='0', row='0', sticky='nw')
        self.frame14.configure(background='#606c38', height='200', width='200')
        self.frame14.grid(column='0', row='0')
        self.frame15 = tk.Frame(self.frame9)
        self.button9 = tk.Button(self.frame15)
        self.button9.configure(background='#8338ec', text='ip-adress.com', width='15',command=self.buttonipaddresscom)
        self.button9.grid(column='0', ipady='3', padx='9', pady='5', row='0')
        self.button16 = tk.Button(self.frame15)
        self.button16.configure(background='#ffd166', text='sslproxies.org', width='15', command=self.buttonsslproxyorg)
        self.button16.grid(column='0', ipady='3', padx='9', pady='5', row='1')
        self.button17 = tk.Button(self.frame15)
        self.button17.configure(background='#ef476f', text='socks-proxy.net', width='15', command=self.buttonsocksproxynet)
        self.button17.grid(column='0', ipady='3', padx='9', pady='5', row='2')
        self.button18 = tk.Button(self.frame15)
        self.button18.configure(background='#ff006e', text='us-proxy.org', width='15', command=self.buttonusproxyorg)
        self.button18.grid(column='1', ipady='3', padx='9', pady='5', row='0')
        self.button20 = tk.Button(self.frame15)
        self.button20.configure(background='#fb5607', text='free-proxy-list.net', width='15',command=self.buttonfreproxylisnet)
        self.button20.grid(column='1', ipady='3', padx='9', pady='5', row='1')
        # self.button21 = tk.Button(self.frame15)
        # self.button21.configure(background='#06d6a0', text='spys.one', width='15')
        # self.button21.grid(column='0', ipady='3', padx='9', pady='5', row='6')
        self.buttoninsert = tk.Button(self.frame15)
        self.buttoninsert.configure(activebackground='#240046',activeforeground='#ffffff',background='#ffb703',font='system', text='insert to lists', width='15', command=self.inserttolists)
        self.buttoninsert.grid(column='1', ipady='3', padx='9', pady='5', row='2')
        self.frame15.configure(background='#606c38', height='200', width='200')
        self.frame15.grid(column='1', row='0')
        self.frame9.configure(background='#606c38', height='200', width='200')
        self.frame9.pack(side='top')
        self.frame13 = tk.Frame(self.getProxyWindow)
        self.loggeproxytproses = tk.Label(self.frame13)
        self.loggeproxytproses.configure(background='#240046', font='system', foreground='#ffb703', pady='9')
        self.loggeproxytproses.configure(text='Ready.....')
        self.loggeproxytproses.pack(fill='both', side='top')
        self.frame13.configure(background='#023047', height='200', width='200')
        self.frame13.pack(fill='both', side='bottom')
        self.getProxyWindow.configure(background='#606c38', height='200', width='200')
        self.getProxyWindow.title('get proxy lists')

        # Main widget
        self.mainwindow = self.getProxyWindow
    
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = ProxyApp()
    def insertolist(list):
        app.tangkaplists(list)
    app.run()

