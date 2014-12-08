# -*- coding: utf-8 -*-
import coin
import time
import json
from api import API,token
import api
import os
import MySQLdb
import copy
robot = API()

ema_list = []
m1 = []
n1 = []
dea = []
    
def ema(n,a):
    count =0
    m =0
    for i in range(1,(n+1)):
       if type(a[0]) is float:
          count += a[-i]*(n-i+1)
       elif len(a[0]) >1 :
          count += a[-i][1]*(n-i+1)
       m +=i
    ema1 = float(count)/float(m)
    return round(ema1,4)
class trade():
    def user_balance(self):
        try:
            self.userbalance  = robot.balance()
            print self.userbalance
            self.free_btc = float(json.loads(self.userbalance)['data']['futures_wallet']['btc'])
            print self.free_btc
        except Exception ,e:
            print e
            pass
    def user_position(self):
        try:
            self.userposition  = robot.position()
            print "self.userposition:%s"%self.userposition
        except Exception,e:
            print e
            pass
        try:
            data = json.loads(self.userposition)['data']
            if isinstance(data,dict) and data.has_key('sell'):
               self.sell_position = float(json.loads(self.userposition)['data']['sell']['5']['total'])
               print "self.sell_position:%s"%self.sell_position
            if isinstance(data,dict) and data.has_key('buy'):
               self.buy_position = float(json.loads(self.userposition)['data']['buy']['5']['total'])
               print "self.buy_position:%s"%self.buy_position
        except Exception ,e:
            print e
            pass
        
    def open_buy_btc(self,rate):
        self.user_balance()
        amount=self.free_btc*20
        print "amount:%s"%amount
        if amount >1:
            order = int(amount)
        elif amount >0.1:
            order = float(int(amount*10))/10
        elif amount >0.01:
            order = float(int(amount*100))/100
        elif amount <0.01:
            return 0
        try:
            print "*** amount:%s"%amount
            e = robot.open_buy(rate,order)
        except Exception,e:
            print e
            pass
    def close_buy_btc(self,rate):
        self.user_position()
        if hasattr(self,'buy_position'):
            try:
                e = robot.close_buy(rate,self.buy_position)
            except Exception,e:
                print "close_buy_btc:%s"%e
                pass
    def open_sell_btc(self,rate):
        self.user_balance()
        amount=self.free_btc*20
        if amount >1:
            order = int(amount)
        elif amount >0.1:
            order = float(int(amount*10))/10
        elif amount >0.01:
            order = float(int(amount*100))/100
        elif amount < 0.01:
            return 0
        try:
            e = robot.open_sell(rate,order)
        except Exception,e:
            print e
            pass
    def close_sell_btc(self,rate):
        self.user_position()
        if hasattr(self,'sell_position'):
	    try:
	       e = robot.close_sell(rate,self.sell_position)
	    except Exception,e:
	       print e
	       pass

if __name__ == '__main__':
    price = coin.Price()
    price.start()
    time.sleep(5)
    p_list = []
    l =0
    s = 'buy'
    to=token()
    to.get_token()
    flagPrice1 = 0
    flagPrice2 = 0
    dif = []
    dea = []
    bar = []
    btc=trade()
    while(1):
       try:
           t1=time.time()
	   pr=round(coin.p,1)
           p_copy = copy.copy(p_list)
	   if len(p_list) >0 and p_list[-1]!=pr:
	       p_list.append(pr)
	   elif len(p_list)==0:
	       p_list.append(pr)
	   print "len p_list:%s"%len(p_list)
	   if len(p_list) >52:
               if len(p_copy) >0 and p_copy[-1] != p_list[-1]:
                   m1.append(ema(52,p_list))
                   n1.append(ema(3,p_list))
                   dif.append(n1[-1]-m1[-1])
               if len(dif)>8:
                   dea.append(ema(8,dif))
                   bar.append((dif[-1]-dea[-1])*2)
                   if len(dif)>20:
                       dif.pop(0)
                   if len(dea)>5:
                       dea.pop(0)
                       bar.pop(0)
		   print "m1:%s n1:%s"%(m1,n1)
		   if flagPrice1>0 and coin.p < flagPrice1 -1.8 :#and coin.bamount <coin.samount:
                       print "zhisun close_buy_btc"
		       try:
			   btc.close_buy_btc(int(coin.sell))
		       except Exception,e:
			   print "zhisun close_buy_btc error:%s"%e
			   pass
		   elif flagPrice2 > 0 and coin.p > flagPrice2 +1.8 :#and coin.bamount > coin.samount :
                       print "zhisun close_sell_btc"
		       try:
			   btc.close_sell_btc(int(coin.buy))
		       except Exception,e:
			   print "zhisun close_sell_btc error:%s"%e
			   pass
		   if bar[-1] >0 and coin.dt <1200 and coin.vol>30000 :#and coin.bamount > coin.samount :
                       print "close_sell_btc"
		       try:
		           btc.close_sell_btc(int(coin.buy))
		       except Exception,e:
		           print "close_sell_btc error:%s"%e
		           pass
		       print "open_buy_btc"
		       try:
                           print "xxxxxx"
		           flagPrice1 = coin.p
                           print "xxxxxcoin.buy:%s"%coin.buy
		           btc.open_buy_btc(int(coin.buy)+0.01)
                           print "xxxxxxx"
		       except Exception ,e:
		           print "open_buy_btc error:%s"%e
		           pass
		   elif bar[-1]<0 and coin.dt <1200 and coin.vol> 30000 :#and coin.samount > coin.bamount:
                       print "close_buy_btc"
		       try:
		           btc.close_buy_btc(int(coin.sell))
		       except Exception,e:
		           print "close_buy_btc error:%s"%e
		           pass
                       print "open_sell_btc"
		       try:
		           flagPrice2 = coin.p
		           btc.open_sell_btc(int(coin.sell)-0.01)
		       except Exception,e:
		           print "open_sell_btc error:%s"%e
		           pass
		   if flagPrice1 != 0 and coin.p>flagPrice1 :
		       flagPrice1 = coin.p
		   if flagPrice2 != 0 and coin.p<flagPrice2 :
		       flagPrice2 = coin.p
		   print "ssssssssssssssssss bar:%s coin.dt:%s coin.bamount:%s coin.samount:%s coin.buy:%s"%(bar[-1],coin.dt,coin.bamount,coin.samount,coin.buy)
	   if len(m1) > 8:
	       m1.pop(0)
	       n1.pop(0)
           if len(bar)>0:
	       db = MySQLdb.connect("localhost","root","123","ok",charset="utf8")
	       cursor = db.cursor()
	       sql = 'insert into data796 values(%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,null)'%(n1[-1],m1[-1],coin.buy,coin.sell,coin.p,flagPrice1,\
flagPrice2,dif[-1],dea[-1],bar[-1],coin.dt,coin.bamount,coin.samount,coin.vol)
	       try:
	           cursor.execute(sql)
	           db.commit()
	       except Exception,e:
	           print "mysql:%s"%e
	           pass
	   if len(p_list)>52:
	       p_list.pop(0)

	   l+=1
	   if l>20:
	       robot.cancel_all('all')

	   t2=time.time()          
	   if (t2-t1) < 1:
	       time.sleep(1-(t2-t1))
	   cmd = "cat /dev/null > nohup.out"
	   #os.system(cmd)
       except Exception,e:
           time.sleep(1)
           print e
           pass 
