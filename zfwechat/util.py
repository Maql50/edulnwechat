# -*- coding:utf-8 -*-

import hashlib
from lxml import etree
import time
from util import *
from lingnanedu import *
import sys
import urllib2
import urllib
import models
import cookielib

class CheckUtil(object):
	__token = 'wei'

	def checkSignature(self, signature, timestamp, nonce):
		arr = [self.__token, timestamp, nonce]
		arr.sort()
		buffer = ''
		for str in arr:
			buffer += str
			temp = hashlib.sha1(buffer).hexdigest()
		return temp == signature


class MessageUtil(object):
	#收到两种类型的消息，一个关注，二十普通消息
	def type_handler(self, str_xml):
		xml = etree.fromstring(str_xml)

		#被关注消息
		eventElement = xml.find('Event')
		if eventElement is not None:
			xml_str = self.receiveEventMsg(xml)

		#普通消息
		contentElement = xml.find('Content')
		if contentElement is not None:
			xml_str = self.receiveCommonMsg(xml)
		return xml_str

	def receiveCommonMsg(self, xml):
		dict = {}
		dict['FromUserName'] = xml.find('ToUserName').text
		dict['ToUserName'] = xml.find('FromUserName').text
		dict['CreateTime'] = int(time.time())
		dict['Content'] = xml.find('Content').text
		if dict['Content'] == '1':
			xml_str = self.sendLoginMsg(dict)
		elif dict['Content'] == '2':
			xml_str = self.sendAboutMsg(dict)
		else:
			xml_str = self.sendTipsMsg(dict)

		return xml_str

	def sendCommonMsg(self, dict):
		xml_str = '''<xml>
		<ToUserName><![CDATA[%s]]></ToUserName>
		<FromUserName><![CDATA[%s]]></FromUserName>
		<CreateTime>%s</CreateTime>
		<MsgType><![CDATA[%s]]></MsgType>
		<Content><![CDATA[%s]]></Content>
		</xml>''' % (dict['ToUserName'], dict['FromUserName'], dict['CreateTime'], dict['MsgType'], dict['Content'])
		return xml_str

	def receiveEventMsg(self, xml):
		dict = {}
		dict['FromUserName'] = xml.find('ToUserName').text
		dict['ToUserName'] = xml.find('FromUserName').text
		dict['CreateTime'] = int(time.time())
		dict['MsgType'] = 'text'
		dict['Content'] = u'欢迎关注岭师正方微信平台！\n回复：\n  1.<a href="http://dweimaql.tunnel.qydev.com/wechat/login">登录正方系统</a> \n  2.关于本账户'		
		xml_str = self.sendCommonMsg(dict)
		return xml_str		
	
	def sendLoginMsg(self, dict):
		dict['MsgType'] = 'news'
		dict['Title'] = '岭师正方微信登录'
		dict['Description'] = '岭南师范学院正方教务系统微信平台登录'
		dict['PicUrl'] = 'https://www.baidu.com/img/bd_logo1.png'
		dict['Url'] = 'http://dweimaql.tunnel.qydev.com/wechat/login'
		return self.dictToXmlNews(dict)

	def sendAboutMsg(self, dict):
		dict['MsgType'] = 'news'
		dict['Title'] = '关于本账号'
		dict['Description'] = '关于本账号的一点说明'
		dict['PicUrl'] = 'https://www.baidu.com/img/bd_logo1.png'
		dict['Url'] = 'http://mp.weixin.qq.com/s?__biz=MzAwOTgwODc5MQ==&tempkey=dMkY26v8Rd75CPTkFQovft0mbl6NIU57x6xopcM0icpVVsjNQEjYoJSRuHtUNiLrdrrdO2vPm8Ls2sYRSOfHLBPMsOkjrsUaTgJTYLR73tLLPbV5UfvSmr3XZWBY4q75fw4WiidkER0Hhbx0%2BVsibw%3D%3D&#rd'
		return self.dictToXmlNews(dict)

	def sendTipsMsg(self, dict):
		dict['Content'] = u'您好,回复：\n  1.<a href="http://dweimaql.tunnel.qydev.com/wechat/login">登录正方系统</a> \n  2.关于本账户'		
		dict['MsgType'] = 'text'
		xml_str = self.sendCommonMsg(dict)
		return xml_str

	def dictToXmlNews(self, dict):
		xml_str = '''<xml>
			<ToUserName><![CDATA[%s]]></ToUserName>
			<FromUserName><![CDATA[%s]]></FromUserName>
			<CreateTime>%s</CreateTime>
			<MsgType><![CDATA[%s]]></MsgType>
			<ArticleCount>1</ArticleCount>
			<Articles>
			<item>
			<Title><![CDATA[%s]]></Title> 
			<Description><![CDATA[%s]]></Description>
			<PicUrl><![CDATA[%s]]></PicUrl>
			<Url><![CDATA[%s]]></Url>
			</item>
			</Articles>
			</xml>''' % (dict['ToUserName'], dict['FromUserName'], dict['CreateTime'], dict['MsgType'], dict['Title'], dict['Description'], dict['PicUrl'], dict['Url'])
		return xml_str

class WechatUtil(object):
	APPID = "wx0e6cdefb2b1c31af"#"wx72ad5103209497ca"
	APPSECRET = "dacd2ccc518d01445f5056536b042712"#"87c98fdf844ce4215791d89ec25055c7"
	ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET"
	CREATE_MENU_URL = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN"

	def doGetStr(self, url):
		jsonHtml = urllib2.urlopen(url).read()
		return jsonHtml

	def doPostStr(self, url, menu):
		data =  '''{
                 "button":[
                     {    
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "type":"view",
           "name":"歌手简介",
           "url":"http://www.qq.com/"
      },
      {
           "name":"菜单",
           "sub_button":[
            {"type":"click","name":"hello word","key":"V1001_HELLO_WORLD"},{"type":"click","name":"赞一下我们","key":"V1001_GOOD"}]}]}'''
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(cookie))
		myrequest = urllib2.Request(url, data.encode('utf-8'))
		jsonHtml = opener.open(myrequest).read()
		print eval(jsonHtml)

	def getAccessToken(self):
		accessToken = models.AccessToken()
		url = self.ACCESS_TOKEN_URL.replace(
		"APPID", self.APPID).replace("APPSECRET", self.APPSECRET)
		jsonHtml = self.doGetStr(url)
		dict = eval(jsonHtml)
		accessToken._token = dict['access_token']
		accessToken._expiresIn = dict['expires_in']
		return accessToken

	def createMenu(self, token, menu):
		result = -1
		url = self.CREATE_MENU_URL.replace("ACCESS_TOKEN", token)
		jsonDict = self.doPostStr(url, menu);
		if jsonDict != None:
			result = jsonObject.getInt("errcode")
		 
		return result 


if __name__ == '__main__':
    # dict = {"age": 1, "price" : 100, "name" : 'wjw'}
    #print MessageUtil().xmlToDict(MessageUtil().dictToXml('xml', dict))
    token = WechatUtil().getAccessToken()
    print token._token
    print token._expiresIn

    # 20:17
    #token = 'YEVHaeRtsv-hnJSmHH17CQYKa-VqefQgJUv4IjHbqu3ITe0X_4j1-LKrpU2GxP5yKzZkUfqyUZTAy2MRUBK4tnEb9GjY6P9eg0YhUpecYpDFgkjejUOx4q69B2NCDuBySBQfAAAJSH'
    WechatUtil().createMenu(token._token, "")