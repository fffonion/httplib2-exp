#coding:utf-8
import httplib2plus as httplib2,re,os,sys
urllist=['http://acm.hdu.edu.cn/QQ2013/user_view_single.php?oldcid=442&page=','http://acm.hdu.edu.cn/QQ2013/user_view_single.php?oldcid=437&page=','http://acm.hdu.edu.cn/QQ2013/user_view_single.php?oldcid=438&page=','http://acm.hdu.edu.cn/QQ2013/user_view_single.php?oldcid=439&page=','http://acm.hdu.edu.cn/QQ2013/user_view_single.php?oldcid=440&page=','http://acm.hdu.edu.cn/QQ2013/user_view_single.php?oldcid=441&page=']
pageindex=[0,0,0,0,0,0]
if __name__=='__main__':
	ht2=httplib2.Http()
	reload(sys)
	sys.setdefaultencoding('utf-8')
	for url in urllist:
		while 1:
			urlfull=url+str(pageindex[urllist.index(url)])
			print urlfull
			resp,content=ht2.request(urlfull)
			sectors=re.findall('ight_item(.*?)highl',content+'highl',re.DOTALL)
			mon,date=re.findall('(\d)月(\d+)日',content+'highl',re.DOTALL)[0]
			f=open('%s月%s日.csv'%(mon,date),'a')
			if os.path.getsize('%s月%s日.csv'%(mon,date))==0:f.write('GID,姓名,性别,学号,学校,学院,专业,报名时间\n')
			for sec in sectors:
				for i in re.findall('TABLE_TEXT" align="center">(.*?)</td>',sec)[:8]:
					f.write(i+',')
				f.write('\n')
			if pageindex[urllist.index(url)]<(len(re.findall('user_view_single.php',content))-1)/2-1:
				pageindex[urllist.index(url)]+=1
			else:
				break
			f.close()
