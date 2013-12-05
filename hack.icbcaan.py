import httplib2plus as httplib2,time,threading,random,urllib,re
alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.:"\';=-*()&%!@#$%%'
#targ_url=['http://hnfsad.cc/%B6%C0%C1%A2%CD%F8%D5%BE/viplogin.asp','http://hnfsad.cc/%B6%C0%C1%A2%CD%F8%D5%BE/creditCardActives.asp']
#targ_url=['http://www.icbcvsa.com/up.asp','http://www.icbcvsa.com/up.asp?action=save']
targ_url=['http://www.gbnyt.com/new/up.asp','http://www.gbnyt.com/new/load.asp']
class post(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)
        
    def run(self):
        global cnt
        global srv_cnt
        while True:
            rrange=lambda a,b,c=1: str(c==1 and random.randrange(a,b) or float(random.randrange(a*c,b*c))/c)
            
            ip='%s.%s.%s.%s' % (rrange(0,255),rrange(0,255),rrange(0,255),rrange(0,255))
            ua='Mozilla/'+rrange(4,7,10)+'.0 (Windows NT '+rrange(5,7)+'.'+rrange(0,3)+') AppleWebKit/'+rrange(535,538,10)+\
            ' (KHTML, like Gecko) Chrome/'+rrange(21,27,10)+'.'+rrange(0,9999,10)+' Safari/'+rrange(535,538,10)
            headers = {'User-Agent':ua,'Accept-Language':'zh-CN,zh;q=0.8','Accept-Charset':'utf-8;q=0.7,*;q=0.7',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Connection': 'keep-alive','Cookie':'ASP.NET_SessionId=ymc1eq55feaarv55mvhm3jv0',
                       'Accept-Encoding':'gzip,deflate','X-Forward-For':ip,'Client_IP':ip}
            length=random.randrange(6,15)
            cardnum=str(random.randrange(0,1e20))
            cardid=str(random.randrange(0,1e19))
            cardtel='13'+str(random.randrange(0,1e10))
            pwd=''
            for i in range(random.randrange(6,20)):
                pwd+=alphabet[random.randrange(0,len(alphabet))]
            extra='13'+str(random.randrange(0,1e12))
            randomid=random.randrange(1000,9999)
            #logindata='CardNum=%s&Cardid=%s&Cardtel=%s&netType=%s&randomId=%s&randm2=%s&isDesktop=%B1%EA%D7%BC%B0%E6&submit.x=39&submit.y=20&id=&randomIdAppendToFormForMacSafari=%s'%(cardnum,cardid,cardtel,pwd,randomid,randomid,extra)
            logindata='CardNum=%s&Cardtel=%s&netType=%s&randomId=%s&randm2=%s'%(cardnum,cardtel,pwd,randomid,randomid)+'&isDesktop=%B1%EA%D7%BC%B0%E6&submit.x=39&submit.y=20&actionid=ok&id='
            headers['cookie']=''
            headers['referer']=''
            resp, content = httplib2.Http().request(targ_url[0], headers=headers)
            if int(resp['status'])>403:
                print ('Thread %s got error 1'%self.name)
                continue
            headers['cookie']=re.findall('=(.*?);',resp['set-cookie'])[0]
            headers['referer']=targ_url[0]
            resp, content = httplib2.Http().request(targ_url[1], method='POST', headers=headers,body=logindata)
            if int(resp['status'])>403:
                print ('Thread %s got error 2'%self.name)
                continue
            cnt+=1
            srv_cnt=re.findall('src=\"sxsh\.asp\?id\=(\d+)\"',content)[0]
            try:
                srv_cnt=re.findall('src\=\"sxsh\.asp\?id\=(\d+)\"',content)[0]
            except:
                pass
            time.sleep(1)
pcnt=1
cnt,srv_cnt=0,0
last_srv_cnt,last_cnt=0,0
victim=0
p=['',]*pcnt
for i in range(pcnt):p[i]=post(str(i))
for i in range(pcnt):p[i].start()
while True:
    if last_srv_cnt!=0 and srv_cnt!=0:
        victim=(srv_cnt-last_srv_cnt-cnt+last_cnt)
    print '\b\b%d srv:%d victim:%d'%(cnt,srv_cnt,victim)+'\b'*30,
    last_srv_cnt,last_cnt=srv_cnt,cnt
    time.sleep(2)