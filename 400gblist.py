#coding:gbk
import httplib2plus as httplib2
import re
url='http://www.400gb.com/u/1290266/1996046/%d'
start=1
end=17
res=''
http=httplib2.Http()
for i in range(start,end+1):
	print('%d/%d'%(i,end))
	resp,cont=http.request(url%i)
	list=re.findall('http://www.400gb.com/file/\d+',cont)
	list=[list[2*i] for i in range(len(list)/2)]
	res+='\n'.join(list)+'\n'
open('400gb.txt','w').write(res)
	