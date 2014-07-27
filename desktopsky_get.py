#coding:utf-8
import httplib2
import re
import time
import random
import os, os.path as opath
from threading import Thread, RLock
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty
import _headers
base_url = 'http://www.desktopsky.com/dongmanbizhi/Fractale-7361.html'
save_dir = 'z:/'
thread_count = 5
parse_finnished  = False
pic_queue = Queue()
plock = RLock()

def tprint(string):
    plock.acquire()
    print(string)
    plock.release()

class downloader(Thread):
    def __init__(self, iid = None):
        Thread.__init__(self, name = 'D-%s' % iid)
        self._exit = False
        self._dead = False
        self.http = httplib2.Http()

    def tprint(self, string):
        tprint('%s - %s' % (self.name, string))

    def run(self):
        while not self._exit:
            try:
                p = pic_queue.get(False)
                _f = re.findall('[^/]+\.\w{3}', p)[1]
                fname = opath.join(save_dir, name, _f)
                if opath.exists(fname) and os.stat(fname).st_size:
                    self.tprint('skip %s' % _f)
                    continue
                _ = self.http.request(p, headers = headers)[1]
                open(fname, 'wb').write(_)
                self.tprint('done %s' % _f)
            except Empty:
                if parse_finnished:
                    self._dead = True
                    self.tprint('bye~')
                    break
                else:
                    time.sleep(random.random() * 2)


ht = httplib2.Http()
headers = _headers.get()
_index = ht.request(base_url, headers = headers)[1].decode('gbk')
name = re.findall('h1\>(.+)\<\/h1', _index)[0][:-2]
count = len(re.findall('/li', re.findall('paginator.*?</ul>', _index, re.DOTALL)[0])) - 3
if count < 0:
    count = 1
print('%s total:%d pages' % (name, count))
if not opath.exists(opath.join(save_dir, name)):
    os.mkdir(opath.join(save_dir, name))
all_thread = []
for i in range(thread_count):
    t = downloader(i)
    all_thread.append(t)
    t.setDaemon(True)
    t.start()

cur_idx = 1
page = _index
pcnt = 0
while cur_idx <= count:
    pics = re.findall('http://img.desktopsky.com/uploads/allimg/.+-lp.jpg', page)
    for p in pics:
        pic_queue.put(p.replace('-lp', ''), False)
        pcnt += 1
    tprint('parse finnished on page %d' % cur_idx)
    cur_idx += 1
    page = ht.request(base_url.replace('.html', '_%d.html' % cur_idx), headers = headers)[1].decode('gbk')
tprint('parse finnished %dp' % pcnt)

parse_finnished = True
while sum(map(lambda x:0 if x._dead else 1, all_thread)):
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        for p in all_thread:
            p._exit = True
        break

for p in all_thread:
    p.join()