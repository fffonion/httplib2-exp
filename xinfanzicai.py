#coding:utf-8
import httplib2
import json
import time
ht=httplib2.Http()
#print re.findall('\[torrent\=(\d+)\]',a)
url='http://www.kmgtp.org/cake/torrents/delete/%s.json'
ids=['84415', '87351', '88504', '83833', '87025', '85513', '85083', '92193', '82578', '89487', '90232', '87947', '86659', '91379', '82511']
errs=[]
permdny=[]
for i in ids:
    print i,
    resp,ct=ht.request(url%i,method='POST',headers={'Referer':'http://www.kmgtp.org/details.php?id=%s'%i,'content-type':'application/x-www-form-urlencoded; charset=UTF-8','cookie':'c_secure_uid=NzY2NjI%3D; c_secure_pass=220f7a2f9f8f05913def71fb5d66b86a; c_secure_ssl=bm9wZQ%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_login=bm9wZQ%3D%3D',},body="_method=DELETE&data[reasonType]=4&data[reasonDetail]=%E6%96%B0%E7%95%AA%E8%87%AA%E8%A3%81")
    try:
        print 'res:%s msg:%s'%(json.loads(ct)['success'],json.loads(ct)['message'])
        if json.loads(ct)['message']=='You can\'t delete this torrent.':
            permdny.append(i)
        elif json.loads(ct)['success']==False:
            errs.append(i)
    except KeyError:
        print json.loads(ct)['name']
        errs.append(i)
    # except ValueError:#not json
    #     print ct
    time.sleep(0.5)

print 'error:\n%s'%(','.join(errs))
print 'permision denied:\n%s'%(','.join(permdny))