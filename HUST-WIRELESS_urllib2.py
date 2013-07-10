#!/usr/bin/python
# -*- coding:utf-8 -*-
# HUST-WIRELESS autologin script, urllib2 version
# Contributor:
#      fffonion        <fffonion#gmail.com>

import re
import os
import sys
import base64
import getpass
import urllib2

__version__=1.2
id,pswd,save_pswd='','',False
session_file='.HUST-WIRELESS.session'
id_file='.HUST-WIRELESS.id'
testurl='http://www.baidu.com/'
loginstr='/eportal/userV2.do?method=login'
logoutstr='/eportal/userV2.do?method=logout'
header={'Content-Type':'application/x-www-form-urlencoded'}
#handle sys.argv
if os.path.exists(id_file):
	id,pswd=base64.decodestring(open(id_file).read()).split(',')
	if pswd!='':
		save_pswd=True
if len(sys.argv)>1:
	if sys.argv[1]=='help' or sys.argv[1]=='-h' or sys.argv[1]=='--help':
		#help message
		print('HUST-WIRELESS login utilty writing in python using urllib2\nUsage:\tloginHUST-WIRELESS.py [-sc]\n\tloginHUST-WIRELESS.py username [-sc]\n\tloginHUST-WIRELESS.py username pswd [-sc]\nArgs:\t-s\tSave password (username is automatically saved)\n\t-c\tClean saved username and password\nNotes:\tSaved pswd is only softly protected, be cautious!\n\tCLI input overrides saved account.')
		os._exit(0)	
	if len(sys.argv)>2 and not sys.argv[2].startswith('-'):
		pswd= sys.argv[2]
	if not sys.argv[1].startswith('-'):#judge if is extra args
		if id!=sys.argv[1]:#new username?
			pswd=''#clean saved
			id=sys.argv[1]
	if sys.argv[-1].startswith('-'):
		if 's' in sys.argv[-1]:#save
			save_pswd=True
		if 'c' in sys.argv[-1]:#clean
			if os.path.exists(id_file):
				os.remove(id_file)
				print('Account info deleted.')
			else:
				print('No account info to delete.')
#test some url
ct=urllib2.urlopen(testurl).read()
#open('z:\\123.htm','a').write(ct)
# url being wanted is encrypted here, need more research
url=re.findall('self.location.href=\'([^\']+)\'',ct)
if url==[]:
	#logout process
	#read session file
	if not os.path.exists(session_file):
		print('You\'ve connected to Internet, but it seems you are not using HUST-WIRELESS ?')
	else:
		host_url,args=open(session_file,'r').read().split(',')
		#logout
		ct=urllib2.urlopen('%s%s&%s'%(host_url,logoutstr,args)).read()
		if re.findall('window\.location\.replace\("\.\/userV2\.do\?method=goToLogout"\);',ct)!=[]:
			print('Logout succeed!')
		#session no longer avaliable
		if os.path.exists(session_file):
			os.remove(session_file)
else:
	#login process
	url=url[0]
	#split ip and path
	post_url,args=url.split('?')
	host_url=post_url.replace('/eportal/index.jsp','')#ip address
	#write session args to file for logout
	open(session_file,'w').write(','.join([host_url,args]))
	#prompt for input
	id=id or raw_input('username >')
	pswd=pswd or getpass.getpass('password for %s >'%id)
	#save pswd and id
	open(id_file,'w').write(base64.encodestring(','.join([id,save_pswd and pswd or ''])))
	#POST args without url, we don't need that
	args='%s&username=%s&pwd=%s&validcode=no_check'%(args[:(args.find('url')-1)],id,pswd)
	#do the POST
	req=urllib2.Request('%s%s'%(host_url,loginstr))
	ct=urllib2.urlopen(req,args).read()
	#test if successful
	if re.findall('window.location.replace\("\.\/userV2\.do\?method=goToAuthResult',ct)!=[]:
		print('Login succeed!')
	else:
		errmsg=re.findall('errorMessage.innerHTML = \'<strong>(.+)</strong>',ct)[0]
		print('Login failed: %s'%errmsg)
if len(sys.argv)==1:
	raw_input('Press Enter to exit...')