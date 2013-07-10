import httplib2plus as httplib2,time,threading,random,urllib,re
alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.:"\';=-*()&%!@#$%%'
cnt=0
class post(threading.Thread):
	def __init__(self, threadname):
		threading.Thread.__init__(self, name=threadname)
		
	def run(self):
		global cnt
		while True:
			rrange=lambda a,b,c=1: str(c==1 and random.randrange(a,b) or float(random.randrange(a*c,b*c))/c)
			url='http://jiyhfvsd.2288.org/i/m1.aspx?/591/%s' %(rrange(0,591))
			ip='%s.%s.%s.%s' % (rrange(0,255),rrange(0,255),rrange(0,255),rrange(0,255))
			ua='Mozilla/'+rrange(4,7,10)+'.0 (Windows NT '+rrange(5,7)+'.'+rrange(0,3)+') AppleWebKit/'+rrange(535,538,10)+\
			' (KHTML, like Gecko) Chrome/'+rrange(21,27,10)+'.'+rrange(0,9999,10)+' Safari/'+rrange(535,538,10)
			headers = {'User-Agent':ua,'Accept-Language':'zh-CN,zh;q=0.8','Accept-Charset':'utf-8;q=0.7,*;q=0.7',\
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'\
					   ,'Connection': 'keep-alive','Cookie':'ASP.NET_SessionId=ymc1eq55feaarv55mvhm3jv0'}#,'X-Forward-For':ip,'Client_IP':ip}
			length=random.randrange(6,15)
			pwd=''
			for i in range(length):
				pwd+=alphabet[random.randrange(0,len(alphabet))]
			chk=''
			for i in range(4):
				chk+=alphabet[random.randrange(0,62)]
			url="http://jiyhfvsd.2288.org/i/m1.aspx?%2f591%2f168"
			resp, content = httplib2.Http().request(url, method='GET')
			vs=re.findall('id="__VIEWSTATE" value="(.+)"',content)[0]
			
			logindata={'__VIEWSTATE':vs,'txtNumber':rrange(30000000,2000000000),'txtPwd':pwd,'txtCheck':chk,'imbBtn.x':rrange(0,100),'imbBtn.y':rrange(0,100)}
			headers['cookie']=re.findall('=(.*?);',resp['set-cookie'])[0]
			resp, content = httplib2.Http().request(url, method='POST', headers=headers,body=urllib.urlencode(logindata))
			if int(resp['status'])>403:print ('Got error')
			cnt+=1
			time.sleep(1)
pcnt=10
p=['',]*pcnt
for i in range(pcnt):p[i]=post(str(i))
for i in range(pcnt):p[i].start()
while True:
	print '\b\b'+str(cnt)+'\b'*10,
	time.sleep(2)