#coding:gbk
import httplib2
import re
import _headers
import os
#from urlparse import urljoin
class pcgames(object):
    def __init__(self,index='',oristart=''):
        self.url=index
        self.oristart=oristart
        self.ht=httplib2.Http()
        self.baseurl='http://photos.pcgames.com.cn/'
        self.piclist=[]
        self.name=''

    def getpics(self):
        if self.url:self._getpics_index()
        elif self.oristart:self._getpics_ori()
        else:raise Exception('No url specified.')
        
    def _getpics_index(self):
        picpagelist=[]
        oripagelist=[]
        resp,content=self.ht.request(self.url,headers=_headers.get())
        self.name=re.findall('<h1>(.+)</h1',content)[0].strip()
        print self.name
        picarea=re.findall('div class="listnr">(.*?)</div',content,re.DOTALL)[0]
        for sec in re.findall('li>(.*?)</li',picarea,re.DOTALL):
            picpagelist.append(self.absurl(re.findall('href="(.*?)"',sec)[0]))
        print('Done gathering %d pages.' % len(picpagelist))
        
        for url in picpagelist:
            rs,ct=self.ht.request(url,headers=_headers.get())
            oripagelist.append(self.absurl(re.findall('href="(.+)" class="in2"',ct)[0]))
        print('Done loading %d pages.' % len(oripagelist))
        
        for url in oripagelist:
            self.piclist.append(self._parseori(url)[0])
        print('Done loading %d image urls.' % len(self.piclist))
        
    def _parseori(self,url):
        rs,ct=self.ht.request(url,headers=_headers.get())
        picurl=re.findall('<img id="on_img".*?src="(.*?)"',ct,re.DOTALL)[0]
        nexturl=re.findall('<a href="(.*?)"',ct)
        nexturl= nexturl==[] and '' or ('http://photos.pcgames.com.cn/source/'+nexturl[0])
        cur,total=re.findall('<i>(\d+)</i>.*?<i>(\d+)</i>',ct)[0]
        if not self.name:
            self.name=re.findall('<b>(.*?)</b></a></span><span class="page">',ct)[0].strip()
            print(self.name)
        if cur==total:nexturl=''
        return picurl,nexturl,cur,total
    
    def _getpics_ori(self):
        if not self.oristart:return
        next=self.oristart
        while next:
            self.piclist.append('')
            self.piclist[-1],next,cur,total=self._parseori(next)
        print('Done loading %d image urls.' % len(self.piclist))
    
    def download(self,dir=''):
        dir=os.path.join(dir,self.name).decode('gbk')
        if not os.path.exists(dir):os.mkdir(dir)
        total=len(self.piclist)
        for i in range(total):
            picname=re.findall('.+/(.+)',self.piclist[i].rstrip('/'))[0]
            print('Downloading %2d/%2d images: %s' %(i+1,total,picname))
            open(os.path.join(dir,picname),'wb').write(self.ht.request(self.piclist[i])[1])
            
    def absurl(self,url):
        return url.replace('..',self.baseurl)
        
if __name__=='__main__':
    #p=pcgames(index='http://photos.pcgames.com.cn/photolist/30368.html')
    u=raw_input('URL > ')
    if u.startswith('http://photos.pcgames.com.cn/photolist'):
        p=pcgames(index=u)
    else:
        p=pcgames(oristart=u)
    dir=raw_input('DIR > ')
    p.getpics()
    p.download(dir)