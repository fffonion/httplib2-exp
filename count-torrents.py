#coding:utf-8
import httplib2
import base64
ht=httplib2.Http()
coo=raw_input('input cookie >')
resp,ct=ht.request('http://www.kmgtp.org/getusertorrentlistajax.php?userid=%s&type=uploaded'%uid,headers={'Cookie':coo})
print resp
print ct
#'(http\://www\.kmgtp\.org/details\.php\?id=.*?) title="(.*?)"
#fb323c416b18a8019f5ac7f1da9f7bfa->111111
#d4fc49c67e0fcd3eb4e1080f70d82e10->222222
#77368fa2dae138a70e5dbefad63acc52 ->hudbt.ldh34jchs2