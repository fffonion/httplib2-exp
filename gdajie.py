#coding:gbk
import httplib2plus as httplib2,re,urllib,sys
import _headers
import clipboard
if len(sys.argv)>1:topicid=sys.argv[1]
else:topicid=raw_input('输入topicid或者网址 >')
if topicid.startswith('http'):topicid=re.findall('.+/(\d+)/*',topicid.rstrip('/'))[0]
url='http://verycd.gdajie.com/topics/%s' %topicid
resp, content = httplib2.Http().request(url, method='GET',headers=headers)
list=re.findall('<font color="red".*?href="(.*?)".*?</font>',content,re.DOTALL)
str=''
for li in list:
	if not li.startswith('http://www.verycd.gdajie.com/detail.htm'):continue
	content = httplib2.Http().request(li, method='GET',headers=_headers.get())[1]
	strp=re.findall("var ed2k_links = '(.+)';",content)[0]
	str+=(strp+'\n')
	print urllib.unquote(strp).decode('utf-8')
clipboard.SetClipboardText(str)
raw_input('\n抓取完成并已复制到剪贴板XD')