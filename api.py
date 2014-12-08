#-*- coding:utf-8 -*-
import urllib2
from urllib import quote,urlencode
import json
import time
import uuid
import hmac, hashlib
import base64
import httplib
def open_url(url):
    while(1):
      try:
          print "open_url:%s"%url
          data = urllib2.urlopen(url,data='',timeout=5).read()
          print "ssss:%s"%data
          if  json.loads(data).has_key('errno') :
              if json.loads(data)['errno'] == "0":
                 return data
                 break
              elif json.loads(data)['errno'] == "-102":
                   to = token()
                   to.get_token()
              elif json.loads(data)['errno'] in ["-15","-105","-2","-107"]:
                 print "error:%s"%json.loads(data)['errno']
                 break
              else:
                 continue
          else:
              print "xxs"
              print data
              return data
      except Exception ,e:
          print "open_url:%s"%e
          time.sleep(1)
          continue
      else:
          print "test"
          break
class token:
    def __init__(self):
        self.URL = 'https://www.796.com/oauth/token'
        self.APP_KEY = '6744fe79-ff69-8814-3e3d-6295-54debecc'
        self.APP_SECRET = 'SAp/bEx41ble+4t9eVzIzG4VEknZFJRfs58O/B29RfQDwSKkGoYRKBF2vu89'
        self.params = {
              'appid':10566,
              'apikey': self.APP_KEY,
              'secretkey':self.APP_SECRET,
              'timestamp':int(time.time()),
           }
    def get_token(self):
        global access_token ,uid
        sigg = urlencode(sorted(self.params.iteritems(),key=lambda a:a[0],reverse=False))
        reqBody = ''
        p=self.params
        p.pop('secretkey')
        for k in sorted(p.keys()):
           if len(reqBody) > 0:
               reqBody += "&"
           reqBody += (k + "=" + str(self.params[k]))
        sig = quote(
                          base64.b64encode(
                          hmac.new(self.APP_SECRET, sigg, digestmod=hashlib.sha1).hexdigest()
                      ).rstrip())
        h =self.URL+'?'+reqBody+'&'+'sig'+'='+sig
        data = open_url(h)
        print data
        access_token = json.loads(data)['data']["access_token"]
        uid = json.loads(data)['data']["uid"]
        print uid ,access_token
class API:
        def __cancel_order__(self,func,b):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?"+"bs="+b+"&access_token"+"="+access_token
                 return open_url(url)
        def cancel_all(self,b):
                return self.__cancel_order__("cancel_all",b)
        def __info__(self,func):
                 global access_token
                 url = "https://796.com/v1/user/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def get_info(self):
                return self.__info__("get_info")
        def __get_balance__(self,func):
                 global access_token
                 url = "https://796.com/v1/user/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def balance(self):
                return self.__get_balance__("get_balance")
        def __close_buy__(self,func,rate,amount):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?times=5&amount="+"%s"%amount+"&price="+"%s"%rate+"&access_token="+access_token
                 return open_url(url)
        def close_buy(self,rate,amount):
                return self.__close_buy__("close_buy",rate,amount)
        def __open_buy__(self,func,rate,amount):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?times=5&buy_num="+"%s"%amount+"&buy_price="+"%s"%rate+"&access_token="+access_token
                 return open_url(url)
        def open_buy(self,rate,amount):
                return self.__open_buy__("open_buy",rate,amount)
        def __close_sell__(self,func,rate,amount):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?times=5&amount="+"%s"%amount+"&price="+"%s"%rate+"&access_token="+access_token
                 return open_url(url)
        def close_sell(self,rate,amount):
                return self.__close_sell__("close_sell",rate,amount)
        def __open_sell__(self,func,rate,amount):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?times=5&sell_num="+"%s"%amount+"&sell_price="+"%s"%rate+"&access_token="+access_token
                 return open_url(url)
        def open_sell(self,rate,amount):
                return self.__open_sell__("open_sell",rate,amount)

        def __depth__(self,func):
                 global access_token
                 url = "https://796.com/v1/user/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def depth(self):
                return self.__depth__("depth")
        def __trades__(self,func):
                 global access_token
                 url = "https://796.com/v1/user/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def trades(self):
                return self.__trades__("trades")
        def __records__(self,func):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def records(self):
                return self.__records__("records")
        def __orders__(self,func):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def orders(self):
                return self.__orders__("orders")
        def __position__(self,func):
                 global access_token
                 url = "https://796.com/v1/weeklyfutures/"+func+"?"+"access_token"+"="+access_token
                 return open_url(url)
        def position(self):
                return self.__position__("position")
    
"""def btc_detail():
    global buy,sell,p
    btc_price = json.loads(api_get('ticker'))['ticker']
    buy = float(btc_price["buy"])
    sell= float(btc_price["sell"])
    p = float(btc_price["last"])
    print "buy:%s sell:%s p:%s"%(buy,sell,p)"""
if  __name__ == "__main__":
        time.sleep(1)
        a = token()
        a.get_token()
        print "xx"
        x=API()
        e=x.cancel_all("buy")
        print "e:%s"%e
        e=x.balance()
        print "balance:%s"%e 
        e=x.records()
        print "records:%s"%e 
        e=x.orders()
        print "orders:%s"%e 
        e=x.open_buy(1,0.01)
        print "open_buy:%s"%e 
        e=x.close_buy(1,0.01)
        print "close_buy:%s"%e 
        e=x.open_sell(1,0.01)
        print "open_sell:%s"%e 
        e=x.close_sell(1,0.01)
        print "close_sell:%s"%e 
        e=x.position()
        print "position:%s"%e 
