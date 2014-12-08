#-*- coding:utf-8 -*-
import urllib2
import json
import time
import threading
import MySQLdb
class Price(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop =False
        self.__trade__ = "http://api.796.com/v3/futures/trades.html?type=weekly"
        self.__depth__ = "http://api.796.com/v3/futures/depth.html?type=weekly"
        self.__tickers__ = "http://api.796.com/v3/futures/ticker.html?type=weekly"
    def stop(self):
        self.thread_stop = True
    def __get_price__(self,api):
        while(1):
            try:
                content = urllib2.urlopen(api ,timeout=1).read() 
            except Exception ,e:
                print "error:%s"%e
                continue
            return json.loads(content)
    def trade(self):
        trade = self.__get_price__(self.__trade__)
        return trade
    def depth(self):
        depth = self.__get_price__(self.__depth__)
        return depth
    def ticker(self):
        ticker = self.__get_price__(self.__tickers__)
        return ticker 
    def run(self):
        global buy,sell,p,dt,dbid,dask,p10,samount,bamount,vol
        list = []
        while(1):
            try:
                ti= self.ticker()
                vol = float(ti['ticker']['vol'])
                detail = self.depth()
                buy = float(detail["bids"][0][0])
                sell = float(detail["asks"][-1][0])
                t=self.trade()[::-1]
                #print t
                for i in t:
                    if i not in list:
                          list.append(i)
                print len(list)
                count = 0
                amount = 0
		for i in range(-1,-len(list),-1):
		    count += float(list[i]['price'])*float(list[i]['amount'])
		    amount += float(list[i]['amount'])
		    if amount > 10 :
		        p = float(round((count/amount)*3))
			dt = list[-1]['date']-list[i]['date']
			print "p:%s amount:%s dt:%s"%(p,amount,dt)
			bamount = 0
			for j in range(-1,i-1,-1):
			    if list[j]['type'] == 'buy':
				bamount += float(list[j]['amount'])
		        print "bamount:%s"%bamount
			samount = 0
			for j in range(-1,i-1,-1):
			    if list[j]['type'] == 'sell':
				samount += float(list[j]['amount'])
                        print "samount:%s"%samount
                        
                        break
                time.sleep(0.9999)
                if len(list)>3000:
		   list.pop(0)
            except Exception,e:
                print e
                continue

if __name__ == "__main__":
    btc = Price()
    btc.start()
    time.sleep(3)
