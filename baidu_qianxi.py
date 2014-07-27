#coding:utf-8
import httplib2
import datetime
import os, os.path as opath
import time
import random
ht = httplib2.Http('.qianxi')
save_path = 'qianxi_result'
header={'Connection' : ' keep-alive',
'Cache-Control' : ' no-cache',
'Pragma' : ' no-cache',
'User-Agent' : ' Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1797.2 Safari/537.36',
'Accept' : ' */*',
'Referer' : ' htt://qianxi.baidu.com/',
'Accept-Encoding' : ' gzip,deflate,sdch',
'Accept-Language' : ' zh-CN,zh;q=0.8',
'Cookie' : ' BAIDUID=62B339FBEA5F74F542BFD983477B7446:FG=1'}
# header_pic = dict(header)
# header_pic.update({'Cookie' : 'BAIDUID=62B339FBEA5F74F542BFD983477B7446:FG=1; H_PS_PSSID=5042_1427_4263_4760'})
if not opath.exists(save_path):
    os.mkdir(save_path)
#GMT时间 时间+4 得需要时间 2 http://bcscdn.baidu.com/baidu-qianxi/data/20140116_2000.zip 20140117 0点 16日前 default
bcs_base = 'http://bcscdn.baidu.com/baidu-qianxi'
#bcs_pic = 'http://bcscdn.baidu.com/baidu-qianxi/picture/'#2014012818/20140128_1800_china.jpg
#4个defualt手动一下吧233
data_path = opath.join(save_path, 'data')
if not opath.exists(data_path):
    os.mkdir(data_path)
chinap_path = opath.join(save_path, 'china_picture')
if not opath.exists(chinap_path):
    os.mkdir(chinap_path)
for dt in range(20140116,20140132)+range(20140201,int(datetime.datetime.now().strftime('%Y%m%d'))):
    for hr in range(0,2400,100):#0 to 2300
        #json data
        data_reqname = '%d_%04d.zip' % (dt, hr)
        data_fname = '%d_%02d.zip' % (dt + (1 if hr >= 2000 else 0), (hr / 100 + 4) % 24)
        if opath.exists(opath.join(data_path, data_fname)):
            print('Skip %s'%data_fname)
        else:
            resp, ct = ht.request('%s/data/%s'%(bcs_base, data_reqname), headers = header)
            if int(resp['status'])>300:
                print('Error%s %s'%(data_fname, resp['status']))
            else:
                open(opath.join(data_path, data_fname), 'wb').write(ct)
                print('Done %s'%data_fname)
            time.sleep(random.randrange(5,15)/10.0)

        #china picture
        chinap_reqname = '%d_%04d_china.jpg' % (dt, hr)
        chinap_fname = '%d_%02d_china.jpg' % (dt + (1 if hr >= 2000 else 0), (hr / 100 + 4) % 24)
        if opath.exists(opath.join(chinap_path, chinap_fname)):
            print('Skip %s'%chinap_fname)
        else:
            resp, ct = ht.request('%s/picture/%d%02d/%s'%(bcs_base, dt, hr / 100, chinap_reqname), headers = header)
            if int(resp['status'])>300:
                print('Error%s %s'%(chinap_fname, resp['status']))
            else:
                open(opath.join(chinap_path, chinap_fname), 'wb').write(ct)
                print('Done %s'%chinap_reqname)
            time.sleep(random.randrange(5,15)/10.0)