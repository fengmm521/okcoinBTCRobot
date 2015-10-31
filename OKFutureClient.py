#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time
from pyasn1.compat.octets import null
#国际站
class OKFutureClient():
    def __init__(self):
        self.wsocket = 0
        self.timeDelay = int(time.time())
        self.isTradeFutureDataOpen = False
        self.orderFunc = null
        self.getuserinfoFunc = null
        self.lastorderstr = ''
        self.lastuserinfo = ''
    #设置客户端websocket
    def setWebSocket(self,ws):
        self.wsocket = ws
    #期货收报机数据
    def openBTCUSDTicker_quarter(self,contractType = 'quarter'):#默认使用季合约
        if contractType == 'quarter':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_ticker_quarter','binary':'true'}")
        elif contractType == 'this_week':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_ticker_this_week','binary':'true'}")
        elif contractType == 'next_week':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_ticker_next_week','binary':'true'}")
    #期货成交数据推送
    def openTradeFutureData(self,contractType = 'quarter'):#默使用季合约成交数据
        if contractType == 'quarter':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_trade_v1_quarter'}")
        elif contractType == 'this_week':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_trade_v1_this_week'}")
        elif contractType == 'next_week':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_trade_v1_next_week'}")
    #期货深度数据推送
    def openTradeFutureDepthData(self,contractType = 'quarter'):
        if contractType == 'quarter':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_depth_quarter'}");
        elif contractType == 'this_week':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_depth_this_week'}");
        elif contractType == 'next_week':
            self.wsocket.send("{'event':'addChannel','channel':'ok_btcusd_future_depth_next_week'}");
    #获取交易历史数据
    def getFutureOrder(self):
        self.wsocket.send(self.orderstr)
    #获取用户信息数据
    def getUserInfo(self):
        self.wsocket.send(self.userinfo)
    #服务器返回数据
    def showData(self,channel,data = 'test'):
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