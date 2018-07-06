#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
from pyasn1.compat.octets import null
#okex
#websocket只用来定阅数据推送，下单使用rest的https接口发送
class OKFutureClient():
    def __init__(self,apikey,secretkey):
        self.wsocket = 0
        self.timeDelay = int(time.time())
        self.isTradeFutureDataOpen = False
        self.orderFunc = null
        self.getuserinfoFunc = null
        self.lastorderstr = ''
        self.lastuserinfo = ''
        self.api_key = apikey
        self.secret_key = secretkey
    #设置客户端websocket
    def setWebSocket(self,ws):
        self.wsocket = ws
    #期货收报机数据
    # ① X值为：btc, ltc, eth, etc, bch,eos,xrp,btg 
    # ② Y值为：this_week, next_week, quarter
    def openFutureTicker(self,X = 'btc',Y = 'quarter'):#默认使用季合约#ok_sub_futureusd_X_ticker_Y
        chanelcmd = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_ticker_%s','binary':'true'}"%(X,Y)
        self.wsocket.send(chanelcmd)
    #期货成交数据推送
    # ① X值为：btc, ltc, eth, etc, bch,eos,xrp,btg 
    # ② Y值为：this_week, next_week, quarter
    def openFutureData(self,X = 'btc',Y = 'quarter'):#默使用季合约成交数据
        chanelcmd = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_trade_%s'}"%(X,Y)
        self.wsocket.send(chanelcmd)
    #期货200深度增量数据推送,
    # ① X值为：btc, ltc, eth, etc, bch,eos,xrp,btg 
    # ② Y值为：this_week, next_week, quarter
    def openFutureDepth200(self,X = 'btc',Y = 'quarter'):
        channelcmd = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s'}"%(X,Y)
        self.wsocket.send(channelcmd);
    #期货完全深度数据推送,
    # ① X值为：btc, ltc, eth, etc, bch,eos,xrp,btg 
    # ② Y值为：this_week, next_week, quarter 
    # ③ Z值为：5, 10, 20(获取深度条数)
    def openFutureDepth(self,X = 'btc',Y = 'quarter',Z = 5):
        channelcmd = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s_%d'}"%(X,Y,Z)
        self.wsocket.send(channelcmd);
    #订阅合约指数
    # ① X值为：btc, ltc, eth, etc, bch,eos,xrp,btg 
    def openFutureIndex(self,X = 'btc'):
        channelcmd = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_index'}"%(X)
        self.wsocket.send(channelcmd);
    #合约预估交割价格
    # ① X值为：btc, ltc, eth, etc, bch,eos,xrp,btg 
    def openFutureForcast(self,X = 'btc'):
        channelcmd = "{'event':'addChannel','channel':'%s_forecast_price'}"%(X)
        self.wsocket.send(channelcmd);

    #以下为个人事件，需要apikey和sign
    #用户登录事件和个人帐户变动推送
    def onUserLogin(self):
        signstr = self.getLoginSign()
        channelcmd = "{'event':'login','parameters':{'api_key':'%s','sign':'%s'}"%(self.api_key,signstr)
        self.wsocket.send(channelcmd);

    def getLoginSign(self):
        sign = 'api_key=' + str(self.secret_key ) + '&secret_key=' + self.secret_key
        return  hashlib.md5((sign).encode("utf-8")).hexdigest().upper()

    #ping服务器查看连接是否断开
    #服务器未断开会返回{"event":"pong"}
    def pingServer(self):
        channelcmd = "{'event':'ping'}"
        self.wsocket.send(channelcmd);

    #服务器返回数据
    def onMassage(self,channel,data = 'test'):
        if channel == '':#市场交易数据获取
            pass
        elif channel == '':#请求交易返回
            pass
        elif channel == '':#市场深度数据
            pass
        elif channel == '':#交易定单查询返回
            pass
        elif channel == '':#用户数据返回
            pass
        elif channel == '':#收报机数据返回
            pass
        elif channel == '':#当前交易定单查询返回
            pass
        elif channel == '':
            pass
        elif channel == '':
            pass
        print data
        ntim = int(time.time())
        if ntim - self.timeDelay >= 5 and (not self.isTradeFutureDataOpen):
            self.timeDelay = ntim
            #self.openTradeFutureData()
            self.isTradeFutureDataOpen = True
            self.getFutureOrder()
            #self.getUserInfo()
            #self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_ticker_quarter','binary':'true'}")