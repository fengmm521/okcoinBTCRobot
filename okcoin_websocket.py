#!/usr/bin/env python
# -*- coding: utf-8 -*-
import websocket
import OKFutureClient
import time
import sys
import json
import hashlib
import zlib
import base64
from OpenSSL.crypto import sign


api_key='your api_key which you apply'
secret_key = "your secret_key which you apply"
clientx = OKFutureClient.OKFutureClient()

#business
def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    return  hashlib.md5((sign+'secret_key='+secretKey).encode("utf-8")).hexdigest().upper()
#spot trade
def spotTrade(channel,api_key,secretkey,symbol,tradeType,price='',amount=''):
    params={
      'api_key':api_key,
      'symbol':symbol,
      'type':tradeType
     }
    if price:
        params['price'] = price
    if amount:
        params['amount'] = amount
    sign = buildMySign(params,secretkey)
    finalStr =  "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"',\
                'sign':'"+sign+"','symbol':'"+symbol+"','type':'"+tradeType+"'"
    if price:
        finalStr += ",'price':'"+price+"'"
    if amount:
        finalStr += ",'amount':'"+amount+"'"
    finalStr+="},'binary':'true'}"
    return finalStr

#spot cancel order
def spotCancelOrder(channel,api_key,secretkey,symbol,orderId):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'order_id':orderId
    }
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"','symbol':'"+symbol+"','order_id':'"+orderId+"'},'binary':'true'}"

#subscribe trades for self
def realtrades(channel,api_key,secretkey):
    params={'api_key':api_key}
    sign=buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'},'binary':'true'}"

# trade for future
def futureTrade(api_key,secretkey,symbol,contractType,price='',amount='',tradeType='',matchPrice='',leverRate=''):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'contract_type':contractType,
      'amount':amount,
      'type':tradeType,
      'match_price':matchPrice,
      'lever_rate':leverRate
    }
    if price:
        params['price'] = price
    print params
    sign = buildMySign(params,secretkey)
    finalStr = "{'event':'addChannel','channel':'ok_futuresusd_trade','parameters':{'api_key':'"+api_key+"',\
               'sign':'"+sign+"','symbol':'"+symbol+"','contract_type':'"+contractType+"'"
    if price:
        finalStr += ",'price':'"+price+"'"
    finalStr += ",'amount':'"+amount+"','type':'"+tradeType+"','match_price':'"+matchPrice+"','lever_rate':'"+leverRate+"'},'binary':'true'}"
    return finalStr

#future trade cancel
def futureCancelOrder(api_key,secretkey,symbol,orderId,contractType):
    params = {
      'api_key':api_key,
      'symbol':symbol,
      'order_id':orderId,
      'contract_type':contractType
    }
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'ok_futuresusd_cancel_order','parameters':{'api_key':'"+api_key+"',\
            'sign':'"+sign+"','symbol':'"+symbol+"','contract_type':'"+contractType+"','order_id':'"+orderId+"'},'binary':'true'}"

#subscribe future trades for self
#获取期货实时交易单
def futureRealTrades(api_key,secretkey):
    params = {'api_key':api_key}
    sign = buildMySign(params,secretkey)
    return "{'event':'addChannel','channel':'ok_usd_future_realtrades','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'},'binary':'true'}"

#获取期货交易记录，1，已成交，2，未成交
def futureTradeOrder(apikey,secretkey,symbol='btc_usd',orderID='-1',contractType='quarter',status='1',current_page='1',page_length='5'):
    params = {
       'api_key': apikey,
       'symbol': 'btc_usd',
       'order_id':orderID,
        'contract_type': contractType,
        'status': status,
        'current_page': current_page,
        'page_length': page_length
    }
    print sorted(params.keys())
    print params
    sign = buildMySign(params,secretkey)
    print 'md5=',sign 
    finalStr = "{'event':'addChannel', 'channel':'ok_futureusd_order_info', 'parameters':{ " 
    finalStr += "'api_key':'" +apikey+"'," 
    finalStr += "'symbol':'"+ symbol +"',"
    finalStr += "'order_id':'"+orderID+"',"
    finalStr += "'contract_type':'"+ contractType +"',"
    finalStr += "'status':'"+status+"',"
    finalStr += "'current_page':'"+current_page+"',"
    finalStr += "'page_length':'"+page_length+"',"
    finalStr += "'sign':'" + sign +"'}}"
    return finalStr

#用户信息
def userInfo(channel,api_key,secretkey):
    params={'api_key':api_key}
    print params
    sign=buildMySign(params,secretkey)
    usinfstr = "{'event':'addChannel','channel':'"+channel+"','parameters':{'api_key':'"+api_key+"','sign':'"+sign+"'}}"
    print usinfstr
    return usinfstr


def on_open(self):
    #subscribe okcoin.com spot ticker
    #self.send("{'event':'addChannel','channel':'ok_btcusd_ticker','binary':'true'}")
    #subscribe okcoin.com future this_week ticker
    #期货更新数据
    self.send("{'event':'addChannel','channel':'ok_btcusd_future_ticker_quarter','binary':'true'}")#this_week#next_week#
    #期货交易数据
    #self.send("{'event':'addChannel','channel':'ok_btcusd_future_trade_v1_quarter'}")
    #深度{'event':'addChannel','channel':'ok_btcusd_future_depth_quarter'}
    #self.send("{'event':'addChannel','channel':'ok_btcusd_future_depth_quarter'}")
    #subscribe okcoin.com future depth
    #self.send("{'event':'addChannel','channel':'ok_ltcusd_future_depth_next_week','binary':'true'}")

    #subscrib real trades for self
    #realtradesMsg = realtrades('ok_usd_realtrades',api_key,secret_key)
    #self.send(realtradesMsg)


    #spot trade via websocket
    #spotTradeMsg = spotTrade('ok_spotusd_trade',api_key,secret_key,'ltc_usd','buy_market','1','')
    #self.send(spotTradeMsg)


    #spot trade cancel
    #spotCancelOrderMsg = spotCancelOrder('ok_spotusd_cancel_order',api_key,secret_key,'btc_usd','125433027')
    #self.send(spotCancelOrderMsg)

    #future trade
    #futureTradeMsg = futureTrade(api_key,secret_key,'btc_usd','this_week','','2','1','1','20')
    #self.send(futureTradeMsg)

    #future trade cancel
    #futureCancelOrderMsg = futureCancelOrder(api_key,secret_key,'btc_usd','65464','this_week')
    #self.send(futureCancelOrderMsg)

    #subscrbe future trades for self
    
#     self.send(futureRealTradesMsg)
#     orderinfo = userInfo('ok_futureusd_userinfo', api_key, secret_key)
#     websocket.send(orderinfo)

def on_message(self,evt):
    data = inflate(evt) #data decompress
    clientx.showData(data)
    #print (data)
def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

def on_error(self,evt):
    print (evt)

def on_close(self,evt):
    print ('DISCONNECT')

def main():
    url = 'wss://real.okex.com:10440/websocket/okexapi'
#     api_key='your api_key which you apply'
#     secret_key = "your secret_key which you apply"

    websocket.enableTrace(False)
    if len(sys.argv) < 2:
        host = url
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    clientx.setWebSocket(ws)
    clientx.orderstr = futureTradeOrder(api_key, secret_key, 'btc_usd', '-1', 'quarter', '2', '1', '5')
    clientx.userinfo = userInfo('ok_futureusd_userinfo', api_key, secret_key)
    
    print 'xxx'
    ws.run_forever()

if __name__ == "__main__":
    # url = "wss://real.okcoin.com:10440/websocket/okcoinapi"      #if okcoin.cn  change url wss://real.okcoin.cn:10440/websocket/okcoinapi
    
