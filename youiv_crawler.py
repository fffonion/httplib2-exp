#coding:utf-8
import httplib2plus as httplib2
import re
import _headers
import time
import os
import urllib
import win32con, ctypes

""" Abbreviations for readability """
OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
memcpy = ctypes.cdll.msvcrt.memcpy

""" Windows Clipboard utilities """
def GetClipboardText():
    text = ""
    if OpenClipboard(0):
        hClipMem = GetClipboardData(win32con.CF_TEXT)
        GlobalLock.restype = ctypes.c_char_p
        text = GlobalLock(hClipMem)
        GlobalUnlock(hClipMem)
        CloseClipboard()
    return text

def SetClipboardText(text):
    buffer = ctypes.c_buffer(text)
    bufferSize = ctypes.sizeof(buffer)
    hGlobalMem = GlobalAlloc(win32con.GHND, bufferSize)
    GlobalLock.restype = ctypes.c_void_p
    lpGlobalMem = GlobalLock(hGlobalMem)
    memcpy(lpGlobalMem, ctypes.addressof(buffer), bufferSize)
    GlobalUnlock(hGlobalMem)
    if OpenClipboard(0):
        EmptyClipboard()
        SetClipboardData(win32con.CF_TEXT, hGlobalMem)
        CloseClipboard()
def unquote(str):
    return urllib.unquote(str).replace('&amp;','&')
    
home="http://www.youiv.com/"
http=httplib2.Http()
pagest=1
#pageend=467#467
baseurl="http://www.youiv.com/forum.php?mod=forumdisplay&fid=279&&filter=typeid&typeid=%s&page=%d"
cat={'289':'IV','290':'U15','293':'MAG'}
totl={'289':356,'290':105,'293':7}
convms=lambda a:time.strftime('%M:%S', time.localtime(a))
for c in cat:
    file='youiv\\%s.txt'%cat[c]
    analyzed=open(file,'r').read()
    time0=time.time()
    for i in range(pagest,totl[c]+1):
        print('Page %d. Time %s ETA %s'%(i,\
              convms(time.time()-time0),\
              convms((time.time()-time0)*1.0/(i-pagest+1)*(totl[c]+1-pagest))))
        if os.path.exists('youiv\\%d.txt'%(i)):
            continue
        resp,cont=http.request(baseurl%(c,i),headers=_headers.get())
        #http://www.youiv.com/thread-116976-1-1.html
        a=re.findall('(forum\.php\?mod=viewthread.*?)\"',cont)
        thread=[]
        for j in range(len(a)/3):
            thread.append(unquote(a[3*j]))
        print('Single thread parsing start.')
        str=''
        strerr=''
        strnoname=''
        for pg in thread:
            tid=re.findall('tid=(\d+)',pg)[0]
            if tid in analyzed:
                continue
            alert=''
            resp,cont=http.request(home+pg,headers=_headers.get())
            torrent=re.findall("href=\"(http[^\"]*?|forum[^\"]*?)\" target",cont)+['']
            if torrent!=[]:
                while torrent[0].startswith('http://www.discuz.net') or torrent[0].startswith('http://www.comsenz.com') or torrent[0].startswith('http://wpa.qq.com'):
                    torrent=torrent[1:]
                torrent=unquote(torrent[0])
                if not torrent.startswith('http'):
                    torrent=home+torrent
            else:
                torrent=pg
                alert='URL NOT FOUND'
            
            name=re.findall('title\s*>.*\[(.*?\-\d+[a-zA-Z]*)\]',cont)
            if name !=[]:
                name=name[0]
            else:
                alert='NAME NOT FOUND'
            print('%s %s %s'%(name,torrent,alert))
            if alert=='':
                str+='%s %s %s\n'%(name,torrent,tid)
            elif alert=='NAME NOT FOUND':
                strnoname+='%s %s %s\n'%('',torrent,tid)
            else:
                strerr+='%s %s %s\n'%(name,torrent,tid)
        print('%d urls got.'%(len(str.split('\n'))-1))
        open(file,'a').write(str)
        open(file.replace('txt','noname.txt'),'a').write(strnoname)
        open(file.replace('txt','err.txt'),'a').write(strerr)
        #SetClipboardText('\n'.join(tlist))