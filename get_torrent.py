# coding:utf-8
import httplib2
import urllib
import os, os.path as opth
import sys
import random
import re

__version__=1.0
__all__ = ['ktxp','popgo']
__author__='fffonion'

class torrent(object):
    def __init__(self):
        object.__init__(self)
        self.cat = ''
        self.name = ''
        self.url = ''
        self.descrurl = ''
        self.time = ''
        self.length = ''
        self.seedercnt = 0
        self.leechercnt = 0
        self.completecnt = 0
        self.upurl = ''
        self.upname = ''
        self.hash = ''
        self.silent=True

class sites(object):
    def __init__(self, temp = '', pagenum = -1):
        self.starturl = ''
        if temp == '':
            gettemp = lambda: sys.platform == 'win32' and os.environ.get('tmp') or '/tmp'
            temp = opth.join(gettemp(), '.ktxp')
        self.ht = httplib2.Http(temp)
        self.pagenum = pagenum
        self.torrents = []
        self.search_base = ''
        self.homeurl = ''
        self.tracker = []
        self.HASH_NAME = 0
        self.REAL_NAME = 1
        # object.__init__(self)
    

    def _genhender(self):
        rrange = lambda a, b, c = 1: str(c == 1 and random.randrange(a, b) or float(random.randrange(a * c, b * c)) / c)
        ua = 'Mozilla/' + rrange(4, 7, 10) + '.0 (Windows NT ' + rrange(5, 7) + '.' + rrange(0, 3) + ') AppleWebKit/' + rrange(535, 538, 10) + \
        ' (KHTML, like Gecko) Chrome/' + rrange(21, 27, 10) + '.' + rrange(0, 9999, 10) + ' Safari/' + rrange(535, 538, 10)
        # ip='%s.%s.%s.%s' % (rrange(0,255),rrange(0,255),rrange(0,255),rrange(0,255))
        return {'User-Agent':ua, 'Accept-Language':'zh-CN,zh;q=0.8', 'Accept-Charset':'utf-8;q=0.7,*;q=0.7', \
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'\
               , 'Connection': 'keep-alive'}  # ,'X-Forward-For':ip,'Client_IP':ip}
    def _print(self,str):
        print (str.decode('utf-8'))
        
    def search(self, str,ready=False):
        self.starturl = self.search_base + urllib.quote(str)
        if ready:
            self.get_torrents()

    def seturl(self,url,ready=False):
    	self.starturl = url
        if ready:
            self.get_torrents()

    def get_torrents(self,silent=None):
        if not silent:
            silent=self.silent
        if self.starturl == '':
            raise Exception('No info specified. Terminated.')
        pageurl = [self.starturl]
        while pageurl:
            pageurl = self._get_page_torrents(pageurl[0])
            #if not silent : self._print pageurl

    def _legalpath(self, str):
        return str.replace('|', '').replace(':', '').replace('?', '').replace('\\', '').replace('/', '').replace('*', '')\
            .replace('<', '').replace('>', '').decode('utf-8')

    def _htmlescape(self, str):
        def replc(match):
            # self._print match.group(0),match.group(1),match.group(2)
            dict = {'amp':'&', 'nbsp':' ', 'quot':'"', 'lt':'<', 'gt':'>', 'copy':'©', 'reg':'®'}
            # dict+={'∀':'forall','∂':'part','∃':'exist','∅':'empty','∇':'nabla','∈':'isin','∉':'notin','∋':'ni','∏':'prod','∑':'sum','−':'minus','∗':'lowast','√':'radic','∝':'prop','∞':'infin','∠':'ang','∧':'and','∨':'or','∩':'cap','∪':'cup','∫':'int','∴':'there4','∼':'sim','≅':'cong','≈':'asymp','≠':'ne','≡':'equiv','≤':'le','≥':'ge','⊂':'sub','⊃':'sup','⊄':'nsub','⊆':'sube','⊇':'supe','⊕':'oplus','⊗':'otimes','⊥':'perp','⋅':'sdot','Α':'Alpha','Β':'Beta','Γ':'Gamma','Δ':'Delta','Ε':'Epsilon','Ζ':'Zeta','Η':'Eta','Θ':'Theta','Ι':'Iota','Κ':'Kappa','Λ':'Lambda','Μ':'Mu','Ν':'Nu','Ξ':'Xi','Ο':'Omicron','Π':'Pi','Ρ':'Rho','Σ':'Sigma','Τ':'Tau','Υ':'Upsilon','Φ':'Phi','Χ':'Chi','Ψ':'Psi','Ω':'Omega','α':'alpha','β':'beta','γ':'gamma','δ':'delta','ε':'epsilon','ζ':'zeta','η':'eta','θ':'theta','ι':'iota','κ':'kappa','λ':'lambda','μ':'mu','ν':'nu','ξ':'xi','ο':'omicron','π':'pi','ρ':'rho','ς':'sigmaf','σ':'sigma','τ':'tau','υ':'upsilon','φ':'phi','χ':'chi','ψ':'psi','ω':'omega','ϑ':'thetasym','ϒ':'upsih','ϖ':'piv','Œ':'OElig','œ':'oelig','Š':'Scaron','š':'scaron','Ÿ':'Yuml','ƒ':'fnof','ˆ':'circ','˜':'tilde',' ':'ensp',' ':'emsp',' ':'thinsp','‌':'zwnj','‍':'zwj','‎':'lrm','‏':'rlm','–':'ndash','—':'mdash','‘':'lsquo','’':'rsquo','‚':'sbquo','“':'ldquo','”':'rdquo','„':'bdquo','†':'dagger','‡':'Dagger','•':'bull','…':'hellip','‰':'permil','′':'prime','″':'Prime','‹':'lsaquo','›':'rsaquo','‾':'oline','€':'euro','™':'trade','←':'larr','↑':'uarr','→':'rarr','↓':'darr','↔':'harr','↵':'crarr','⌈':'lceil','⌉':'rceil','⌊':'lfloor','⌋':'rfloor','◊':'loz','♠':'spades','♣':'clubs','♥':'hearts','♦':'diams'}
            if match.groups > 2:
                if match.group(1) == '#':
                    return unichr(int(match.group(2)))
                else:
                    return  dict.get(match.group(2), '?')
        htmlre = re.compile("&(#?)(\d{1,5}|\w{1,8}|[a-z]+);")
        return htmlre.sub(replc, str)

    def _download(self, url):
        if not url.startswith('http') and not url.startswith('https'):
            url = self.homeurl + url
        url=self._htmlescape(url)
        resp, content = self.ht.request(url, headers = self._genhender())
        if resp.status >= 400:
            raise Exception('Failed to get content. Error code %d' % resp.status)
        return content

    def _magnet(self, seedhash, tracklist):
        line = ['tr.%d=%d' % (i, tracklist[i]) for i in range(len(tracklist))]
        return 'magnet:?xt=urn:btih:%s&%s' % (seedhash, '&'.join(line))

    def download_torrents(self, torrents = None, dir = '', name = 0, silent = None):
        getname = lambda x, nametype:'%s.torrent' % (nametype == self.REAL_NAME and x.name or x.hash)
        if not torrents:
            torrents = self.torrents
        if not silent:
            silent=self.silent
        dir = opth.abspath(dir)
        if not opth.exists(dir):
            os.mkdir(dir)
        for tr in self.torrents:
            if not silent: self._print ('Downloading %s' % tr.name)
            content = self._download(tr.url)
            open(opth.join(dir, self._legalpath(getname(tr, name))), 'wb')\
            .write(content)

    def _get_page_torrents(self, pageurl):
        pass

class ktxp(sites):

    def __init__(self,silent=True):
        sites.__init__(self)
        self.search_base = 'http://bt.ktxp.com/search.php?keyword='
        self.homeurl = 'http://bt.ktxp.com/'
        self.trackers = ['http://tracker.ktxp.com:6868/announce', 'udp://tracker.ktxp.com:6868/announce']
        self.silent=silent

    def _get_page_torrents(self, pageurl):
        pattern = '<td title="(.*?)">.*?</td>\r\n.*?<td><a href=".*?">(.*?)</a></td>.*?<td class="ltext ttitle"><a href="(.*?)" class="quick-down cmbg"></a><a href="(.*?)" target="_blank">(.*?)</a>.*?</td>\r\n.*?<td>(.*?)</td>\r\n.*?<td class="bts-\d">(.*?)</td>\r\n.*?<td class="btl-\d">(.*?)</td>\r\n.*?<td class="btc-\d">(.*?)</td>\r\n.*?<td><a href="(.*?)".*?>(.*?)</a></td>'
        nextpattren='pages clear space-top.+</a><a href="(.*?)" class="nextprev" target="_self">'
        content = self._download(pageurl)
        open(r'z:/1.htm','w').write(content)
        lpos=content.find('<tbody>')
        hpos=content.find('</tbody>',lpos)
        tlist = content[lpos:hpos]
        tlist=tlist.replace('<span class="keyword">', '').replace('</span>', '').split('</tr>')[:-1]
        for i in tlist:
            self.torrents.append(torrent())
            self.torrents[-1].time, self.torrents[-1].cat, self.torrents[-1].url, \
            self.torrents[-1].descrurl, self.torrents[-1].name, self.torrents[-1].length, \
            self.torrents[-1].seedercnt, self.torrents[-1].leechercnt, self.torrents[-1].completecnt, \
            self.torrents[-1].upurl, self.torrents[-1].upname = re.findall(pattern, i)[0]
            self.torrents[-1].hash = re.findall('([a-z0-9]+).torrent', self.torrents[-1].url)[0]
            self.torrents[-1].name = self._htmlescape(self.torrents[-1].name)
            # if a==[]:self._print i
            # else:self._print a
        return re.findall(nextpattren,content,re.DOTALL)

class popgo(sites):
    
    def __init__(self,silent=True):
        sites.__init__(self)
        self.search_base = 'http://share.popgo.org/search.php?title='
        self.homeurl = 'http://share.popgo.org/'
        self.trackers = ['http://t2.popgo.org:7456/annonce']
        self.silent=silent

    def _get_page_torrents(self, pageurl):
        pattern = '<td title="(.*?)">.*?</td>\r\n.*?<td><a href=".*?">(.*?)</a></td>.*?<td class="ltext ttitle"><a href="(.*?)" class="quick-down cmbg"></a><a href="(.*?)" target="_blank">(.*?)</a>.*?</td>\r\n.*?<td>(.*?)</td>\r\n.*?<td class="bts-\d">(.*?)</td>\r\n.*?<td class="btl-\d">(.*?)</td>\r\n.*?<td class="btc-\d">(.*?)</td>\r\n.*?<td><a href="(.*?)".*?>(.*?)</a></td>'
        nextpattren='pages clear space-top.+</a><a href="(.*?)" class="nextprev" target="_self">'
        content = self._download(pageurl)
        tlist = re.findall('tbody(.+/)tbody', content, re.DOTALL)[0].replace('<span class="keyword">', '')\
        .replace('</span>', '').split('</tr>')[:-1]
        for i in tlist:
            self.torrents.append(torrent())
            self.torrents[-1].time, self.torrents[-1].cat, self.torrents[-1].url, \
            self.torrents[-1].descrurl, self.torrents[-1].name, self.torrents[-1].length, \
            self.torrents[-1].seedercnt, self.torrents[-1].leechercnt, self.torrents[-1].completecnt, \
            self.torrents[-1].upurl, self.torrents[-1].upname = re.findall(pattern, i)[0]
            self.torrents[-1].hash = re.findall('?hash=([a-z0-9]+)', self.torrents[-1].url)[0]
            self.torrents[-1].name = self._htmlescape(self.torrents[-1].name)
            # if a==[]:self._print i
            # else:self._print a
        return re.findall(nextpattren,content,re.DOTALL)
    
if __name__ == '__main__':
    kt = ktxp(silent=False)
    #kt.search('あべ美幸騎士團',ready=True)
    kt.search('11番',ready=True)
    #kt.seturl('http://bt.ktxp.com/sort-12-1.html',ready=True)
    #kt.get_torrents()
    kt.download_torrents(dir = 'torrents', name = kt.REAL_NAME)
    # print kt.starturl
