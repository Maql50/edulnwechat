# encoding:utf-8
import sys
import urllib2
import urllib
import re
import cookielib
from operator import attrgetter
from time import clock
import chardet
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

class Mark(object):
	def __init__(self, year, term, lesson, prop, credit, gradepoint, score):
		self.year = year
		self.term = term
		self.lesson = lesson
		self.prop = prop
		self.credit = credit
		self.gradepoint = float(gradepoint)
		self.score = score

class ZhengFangEduSytem(object):
	'''岭南师范学院正方教务系统工具'''

	def getTable(self, score_html):
		'''获取整个表格'''
		trs = re.search('<table class="datelist" cellspacing="0" cellpadding="3" border="0" id="Datagrid1" style="DISPLAY:block">(.*)</table>',score_html, re.S).group(1)
		return trs;

	def getTr(self,trs):
		'''获取成绩表格内的每一行'''
		list = re.findall(u'<tr>(.*?)</tr>',trs, re.S)
		list.extend(re.findall('<tr class="alt">(.*?)</tr>',trs, re.S))
		return list;		

	def getAllLessonObj(self,score_html):
		'''将个人成绩页面中的成绩转为对象类型'''
		trs = self.getTable(score_html)
		tr_list = self.getTr(trs)

		list_lesson_obj = []
		for tr in tr_list:
			list_td = re.findall(r"<td>(.*?)</td>", tr, re.S)
			if len(list_td) == 0 or len(list_td) == 4:
				 continue
			mark = Mark(list_td[0], list_td[1], list_td[3], list_td[4], list_td[6], list_td[7], list_td[8])
			list_lesson_obj.append(mark)

		return sorted(list_lesson_obj, key = attrgetter('year','term'), reverse=True)
			 
	def getPage(self, url):
		'''获取url对应的html'''
		html_cont = requests.get(url)
		html_cont.encoding = 'utf-8' 
		return html_cont.text

	def getPostPage(self, postdate, headers):
		'''提交post表单'''
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(cookie))
		myrequest = urllib2.Request(url, postdate, headers)
		page = opener.open(myrequest).read()
		return page

	def getViewStatus(self, html_cont):
		'''获取页面viewstatus(该值将作为表单提交到下一个页面)'''
		return re.search('<input type="hidden" name="__VIEWSTATE" value="(.*?)" />', html_cont, re.S).group(1)

	def getName(self, page, id): 
		'''获取学生名字'''
		match = re.search(u'<span id="xhxm">'+id+'  (.*?)同学</span></em>', page.decode('utf-8'), re.S)
		if match is not None:
			return match.group(1)
		return False			

	def gethtml(self, html_score):
		'''将获得的html页面为干净的html'''
		html = ""
		html += ("<html>")
		html += ("<head>")
		html += ('<meta http-equiv="content-type" content="text/html; charset=utf-8" />')
		html += ("</head>")
		html += ("<body>")
		html += ("<table border='1px'>")
		html += self.getTable(html_score)
		html += ("</table>")
		html += ("</body>")
		html += ("</html>")
		return html

	def getLesson(self, id , psw, name):
		'''获取课程表'''
		getdata = urllib.urlencode({
			'xh':id,
			'xm':name.encode('gb2312'),
			'gnmkdm':'N121603'
		})

		head = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'no-cache',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded',
			'Host':'202.192.143.243',
			'Origin':'http://222.24.19.201',
			'Pragma':'no-cache',
			'Upgrade-Insecure-Requests':1,	
			'Referer':'http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xs_main.aspx?'+getdata,
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
			}

		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(cookie))
	 	myrequest = urllib2.Request('http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xskbcx.aspx?'+getdata, None, head)
		#获取第二个登录页面
		loginPage = unicode(opener.open(myrequest).read(), 'gb2312').encode('utf-8')
		getLessonTable = re.search('width="14%">星期四</td><td align="Center" width="14%">星期五</td><td class="noprint" align="Center" width="14%">星期六</td><td class="noprint" align="Center" width="14%">星期日</td>(.*?)</table>', loginPage, re.S).group(1)
		getLessonTable = getLessonTable.replace('''<td colspan="2">早晨</td><td align="Center">&nbsp;</td><td align="Center">&nbsp;</td><td align="Center">&nbsp;</td><td align="Center">&nbsp;</td><td align="Center">&nbsp;</td><td class="noprint" align="Center">&nbsp;</td><td class="noprint" align="Center">&nbsp;</td>''','')
		getLessonTable = getLessonTable.replace('\t</tr><tr>\r\n\t\t\r\n\t</tr>',"")
		getLessonTable = getLessonTable.replace('<td rowspan="4" width="1%">上午</td>','')
		getLessonTable = getLessonTable.replace('<td rowspan="4" width="1%">下午</td>','')
		getLessonTable = getLessonTable.replace('<td rowspan="3" width="1%">晚上</td>','')
		getLessonTable = getLessonTable.replace('<td rowspan="3" width="1%">晚上</td>','')
		getLessonTable = re.subn(r'<td class="noprint" align="Center".*?</td>','',getLessonTable)[0]
		getLessonTable = re.subn(r'<br>周.*?}<br>','-',getLessonTable)[0]
		getLessonTable = re.subn(r'\(停.*?\)','',getLessonTable)[0]
		list_color = ["success", "danger","warning"] 
		for i in range(0, 55):
			getLessonTable = getLessonTable.replace('<td align="Center"', '<td class="'+list_color[i%3]+'"  align="Center" ', 1)	
		getLessonTable = re.subn(r'<td class="\w*"  align="Center" >&nbsp;</td>','<td></td>',getLessonTable)[0]
		getLessonTable = re.subn(r'<td class="\w*"  align="Center"  width="7%">&nbsp;</td>','<td align="Center" width="7%"></td>',getLessonTable)[0]
		getLessonTable = getLessonTable.replace('<br><br>','')
		
		return getLessonTable

	def login(self, id, psw):
		'''学生登录'''

		#初始化基本内容
		url = 'http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/default6.aspx'

		#获取登录页面
		page = self.getPage(url)
		
		#设置post数据
		postdate = urllib.urlencode({
			'__VIEWSTATE':self.getViewStatus(page),
			'tnameXw':'yhdl',
			'tbtnsXw':'yhdl|xwxsdl',
			'txtYhm':id,
			'txtXm':psw,
			'txtMm':psw,
			'rblJs':'(unable to decode value)',
			'btnDl':'(unable to decode value)'
		})

		#设置http头
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
		}

		#设置cookie
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(cookie))
		myrequest = urllib2.Request(url, postdate, headers)
		#获取首页，即第二个页面
		loginPage = opener.open(myrequest).read()
		page = unicode(loginPage, 'gb2312').encode("utf-8") 

		result = self.getName(page, id)
		if  result == False:
			return False	

		return result

	def getAvgGradePoint(self, id, psw, name):
		'''获取学生平均几点'''
		getdata = urllib.urlencode({
			'xh':id,
			'xm':name,
			'gnmkdm':'N121605'
		})

		head = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'no-cache',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded',
			'Host':'202.192.143.243',
			'Origin':'http://222.24.19.201',
			'Pragma':'no-cache',
			'Upgrade-Insecure-Requests':1,	
			'Referer':'http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xs_main.aspx?xh='+getdata,
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
			}

		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(cookie))		
	 	myrequest = urllib2.Request('http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xscjcx.aspx?'+getdata, None, head)
		#获取第二个登录页面
		loginPage = unicode(opener.open(myrequest).read(), 'gb2312').encode('utf-8')

		data = urllib.urlencode({
			"__EVENTTARGET": "",
			"__EVENTARGUMENT":"",
			"__VIEWSTATE":self.getViewStatus(loginPage),
			"Button1":unicode("成绩统计",'utf-8').encode('gb2312'),
			"hidLanguage":"",
			"ddlXN":"",
			"ddlXQ":"",
			"ddl_kcxz":""
		}) 

		myrequest = urllib2.Request('http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xscjcx.aspx?'+getdata,data, head)
		#获取第三个页面，即成绩页面
		
		html = opener.open(myrequest)
		result = unicode(html.read(), 'gb2312').encode('utf-8')
		avgGradePoint = re.search(r'<span id="pjxfjd"><b>(.*?)</b></span></td>', result, re.S).group(1)
		return avgGradePoint


	def getMark(self, id, psw, name):
		'''获取个人成绩'''
		getdata = urllib.urlencode({
			'xh':id,
			'xm':name,#self.getName(page, id),
			'gnmkdm':'N121605'
		})

		print "***********"
		print getdata
		print "***********"


		head = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'no-cache',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded',
			'Host':'202.192.143.243',
			'Origin':'http://222.24.19.201',
			'Pragma':'no-cache',
			'Upgrade-Insecure-Requests':1,	
			'Referer':'http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xs_main.aspx?xh='+getdata,
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
			}

		#进入个人成绩查询页面
		#设置cookie
		cookie = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPHandler(cookie))
	 	myrequest = urllib2.Request('http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xscjcx.aspx?'+getdata, None, head)
		loginPage = unicode(opener.open(myrequest).read(), 'gb2312').encode('utf-8')
 


		data = urllib.urlencode({
			"__EVENTTARGET": "",
			"__EVENTARGUMENT":"",
			"__VIEWSTATE":self.getViewStatus(loginPage),
			"btn_zcj":unicode("历年成绩",'utf-8').encode('gb2312'),
			"hidLanguage":"",
			"ddlXN":"",
			"ddlXQ":"",
			"ddl_kcxz":""
		}) 

		myrequest = urllib2.Request('http://202.192.143.243/(51gpbo45h4ah5yrvylalsu45)/xscjcx.aspx?'+getdata, data, head)
		#获取第四个页面，即成绩页面
		html = opener.open(myrequest)
		result = unicode(html.read(), 'gb2312').encode('utf-8')

		allLessonObj = self.getAllLessonObj(result)
		return allLessonObj