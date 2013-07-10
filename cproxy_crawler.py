import httplib2
import re
import random
#import sys,os
#wp u=jiangzemin&p=jzmjzmjzm&v=2.2.0&t=wp&l=wpl1 2 3 4
rrange = lambda a, b, c = 1: str(c == 1 and random.randrange(a, b) or float(random.randrange(a * c, b * c)) / c)
ip = '%s.%s.%s.%s' % (rrange(0, 255), rrange(0, 255), rrange(0, 255), rrange(0, 255))
headers = {'Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded','X-Forward-For':ip,'Client_IP':ip}
hdstart={'Expect':'100-continue'}
hdtarg={'User-Agent':'Python-urllib/1.17'}
hdstart.update(headers)
hdtarg.update(headers)
start='http://mycdb.sinaapp.com/index.php/Rest/Connect?%s'%rrange(100,999)
targ='http://mycdb.sinaapp.com/index.php/Rest/WPConfig'
qstring='u=jiangzemin&p=jzmjzmjzm&v=2.2.0&t=wp&l=wpl%d'
#http://mycdb.sinaapp.com/index.php/Rest/WPTrafficRevc?&tguid=423b7d8881f061c56b26308e1d744d94&ll=1048757
ht=httplib2.Http()
def get_tguid(wpid):
	resp,ct=ht.request(start,method='POST',headers=hdstart,body=qstring%wpid)
	tguid=re.findall('<tguid>(.+)</tguid>',ct)[0]
	print('using tguid: %s'%tguid)
	return tguid
i=10
fname='appid'
fdl='D:\\Dev\\Python\\Workspace\\httplib2-plus-exp\\'
open('%scproxy_%s.txt'%(fdl,fname),'a')
found_all=open('%scproxy_%s.txt'%(fdl,fname),'r').read().split('|')
found_cnt=len(found_all)
while(True):
	if i>=10:
		tguid=get_tguid(1)
		i=0
	resp,ct=ht.request(targ,method='POST',headers=hdtarg,body='tguid=%s'%tguid)
	print ct
	section=re.findall('\[gae\](.*?)\[',ct,re.DOTALL)[0]
	#found=re.findall('fetchserver.*?=.*?(.+)',section)[0].strip(' ').split('|')
	found=re.findall('appid.*?=.*?(.+)',section)[0].strip(' ').split('|')
	pswd=re.findall('password.*?=.*?(.+)',section)[0].strip(' ')
	if pswd!='19920122':
		print pswd
	for j in found:
		if j not in found_all:
			found_all.append(j)
	print('found %d new %d all: %s'%(len(found_all)-found_cnt,len(found_all),','.join(found)))
	found_cnt=len(found_all)
	open('%scproxy_%s.txt'%(fdl,fname),'w').write('|'.join(sorted(found_all)))
	i+=1
