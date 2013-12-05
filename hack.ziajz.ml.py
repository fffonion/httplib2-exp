import httplib2,time,threading,random,urllib,re
alphabetall='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.:"\';=-*()&%!@#$%%'
alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
alpha_small='abcdefghijklmnopqrstuvwxyz'
cnt=0
class post(threading.Thread):
	def __init__(self, threadname):
		threading.Thread.__init__(self, name=threadname)
		
	def run(self):
		global cnt
		while True:
			rrange=lambda a,b,c=1: str(c==1 and random.randrange(a,b) or float(random.randrange(a*c,b*c))/c)
			ip='%s.%s.%s.%s' % (rrange(0,255),rrange(0,255),rrange(0,255),rrange(0,255))
			ua='Mozilla/'+rrange(4,7,10)+'.0 (Windows NT '+rrange(5,7)+'.'+rrange(0,3)+') AppleWebKit/'+rrange(535,538,10)+\
			' (KHTML, like Gecko) Chrome/'+rrange(21,27,10)+'.'+rrange(0,9999,10)+' Safari/'+rrange(535,538,10)
			headers = {'User-Agent':ua,'Accept-Language':'zh-CN,zh;q=0.8','Accept-Charset':'utf-8;q=0.7,*;q=0.7',\
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'\
					   ,'Connection': 'keep-alive','Cookie':'ASPSESSIONIDQABATTBD=EDAFGBKBEDLACMGNBFKMMGOO; ts_last=/cnen/cn2/index.asp; pgv_pvid=8569850260; pgv_info=ssid=s715155125; ts_uid=2912537625; ts_sid=9825436296','Referer':'http://ziajz.ml/cnen/cn2/index.asp?rnd=%s' %(rrange(0,9999)),'Content-Type':'application/x-www-form-urlencoded'}#,'X-Forward-For':ip,'Client_IP':ip}
			length=random.randrange(6,15)
			pwd=''
			for i in range(length):
				pwd+=alphabet[random.randrange(0,len(alphabet))]
			chk=''
			for i in range(4):
				chk+=alphabet[random.randrange(0,62)]
			url="http://ziajz.ml/cnen/cn2/mb_flow_type.asp"
			qq=rrange(30000000,2000000000)
			
			logindata={'u':qq,'p':pwd,'verifycode':chk,'from_ui':'1','dumy':''}
			resp, content = httplib2.Http().request(url, method='POST', headers=headers,body=urllib.urlencode(logindata))
			if int(resp['status'])>403:
				print ('Got error')
			else:
				print 'sent num:%s pwd:%s'%(qq,pwd)
			cnt+=1
			time.sleep(1)
pcnt=10
p=['',]*pcnt
for i in range(pcnt):p[i]=post(str(i))
for i in range(pcnt):p[i].start()
while True:
	print '\b\b'+str(cnt)+'\b'*10,
	time.sleep(2)