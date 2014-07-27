#coding:gb2312
from __future__ import print_function
import _headers
import httplib2
import re
import os
from subprocess import Popen, PIPE
import time
import Queue
import urllib
import threading
targdir="E:\ACG\Drama\down"
metaurl="Special/p_22.Html"
fixed_pref="刑警803_"
error_file=r'z:/%serror.log'%fixed_pref
he=_headers.get()
ht=httplib2.Http()
q=Queue.Queue()
baseurl="http://www.17ttt.com/"
GET=lambda url:ht.request(baseurl+url,headers=he)
ct=GET(metaurl)[1]
thread_cnt=5
chapters=re.findall("Musiclist/\d+\.html",ct)
title=re.findall("id=\"title\".+<p><b>(.*?)</b></p",ct,re.DOTALL)[0]
has=[]
if os.path.exists(r'z:/%s.txt'%title):
    for l in open(r'z:/%s.txt'%title,'r').readlines():
        q.put(l.rstrip('\n'))
else:
    f=open(r'z:/%s.txt'%title,'w')
    for ch in chapters[::-1]:
        print(ch,end='')
        ct=GET(ch)[1]
        episodes=re.findall("Musicplay/[^\.]+.html",ct)
        for ep in episodes:
            q.put(ep)
            f.write(ep+'\n')
print('Done loading episodes.')
errors=[]
class the_thread(threading.Thread):
    def __init__(self,tid):
        threading.Thread.__init__(self, name=tid)
        self.tid=tid
        self.ht=httplib2.Http()
        self.GET=lambda url:self.ht.request(baseurl+url,headers=he)

    def run(self):
        while True:
            try:
                url=q.get(block=False)
            except Queue.Empty:
                break
            ct=self.GET(url)[1]
            valid=re.findall("src=\"/(getrdkey.asp\?file=.+)\"",ct)[0]
            album=re.findall('href="/Musiclist/\d+\.Html" target="_blank">(.*?)</A>',ct)[0].replace(fixed_pref,'')
            trytime=3
            while trytime>0:
                ct=self.GET(valid.replace(' ','%20'))[1]
                mp3=re.findall("'(.+)'",ct)
                if mp3!=[]:
                    break
                trytime-=1
                print('Thread-%d : Retry')
            if mp3==[]:
                errors.append(url)
                print('Thread-%d : Error parsing-%s'%(self.tid,url))
                continue
            else:
                mp3=mp3[0]
            fname=re.findall("([^/]+.mp3)\?",mp3)[0]
            mp3=urllib.quote(mp3).replace('%3A',':').replace('%3F','?').replace('%3D','=')
            if album.split(" ")[0] not in fname:
                fname=album+"_"+fname
            if(os.path.exists('%s\%s'%(targdir,fname))):
                print('Thread-%d : Skip-%s'%(self.tid,fname))
                time.sleep(0.2)
                continue
            print('Thread-%d : Start-%s'%(self.tid,fname))
            t=time.time()
            # os.system('wget \"%s\" -O \"%s\" -q'%(mp3,fname))
            # if os.path.getsize(fname)==0:
            a,b=self.ht.request(mp3,headers=he)
            if(len(b)<1000):
                q.put(url)
                print('Thread-%d : Error-%s got %d'%(self.tid,fname,len(b)))
                time.sleep(1)
                continue
            open(r"%s\%s"%(targdir,fname),'wb').write(b)
            # else:
            #     os.system('move \"%s\" \"%s\%s\" >nul'%(fname,targdir,fname))
            print('Thread-%d : Done-%s(%ds)'%(self.tid,fname,time.time()-t))
        print('Thread-%d : Exit'%self.tid)
ps=[]
for i in range(thread_cnt):
    p=the_thread(i)
    p.start()
    ps.append(p)

for i in range(thread_cnt):
    ps[i].join()
open(error_file,'w').write('\n'.join(errors))
