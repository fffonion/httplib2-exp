#coding:utf-8
import httplib2
import re
import time
h=httplib2.Http()
def get_hidden_var(html):
    pairs=re.findall('<input type="hidden" name="([^"]*)" id="[^"]*" value="([^"]*)" />',html)
    pair_dict={}
    for p in pairs:
        pair_dict[p[0]]=p[1]
    return pair_dict
def pair_to_str(pairdict):
    res=''
    for p in pairdict:
        res='%s&%s=%s'%(res,p,pairdict[p])
    return res
headerdict={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','Accept-Encoding':'gzip,deflate','Accept-Language':'zh-CN','Connection':'keep-alive','DNT':'1','User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.1.3.1200 Chrome/26.0.1410.43 Safari/537.1'}
headers_post=headerdict.update({'Content-Type':'application/x-www-form-urlencoded'})
aspx_url='http://202.114.18.218/Main.aspx'
ori={'programId':'','txtyq':'0','txtld':'0','Txtroom':''}
inp={'programId':'东区','txtyq':'沁苑东十二舍','txtld':'1层','Txtroom':'105'}
resp,ct=h.request(aspx_url,headers=headerdict)
for action in inp:
    namepairs=get_hidden_var(ct)
    ori[action]=inp[action]
    namepairs.update(ori)
    namepairs.update({'__EVENTTARGET':action})
    resp,ct=h.request(aspx_url,headers=,method='POST',body=pair_to_str(namepairs))
    print resp
    print ct.decode('utf-8')
    print namepairs['__VIEWSTATE']
    raw_input()
resp,ct=h.request(aspx_url,headers=headers_post,body=pair_to_str(namepairs))
print resp
print ct