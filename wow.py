from httplib2 import Http
import random
import time
from threading import Thread
from Queue import Queue, Empty
print_queue = Queue()
rnd = lambda :'0.'+''.join([random.choice('0123456789') for i in range(18)])
cnt = 0
class wo(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.ht = Http()
    def run(self):
        while True:
            try:
                _ = self.ht.request('http://page.vote.qq.com/api.php?id=1327749&subjid=1363334&optidlist=100790|100791&type=result&rdm=' + rnd())[1].split(':')
                print_queue.put([self.name, 'current:%s/%s [%d]' % (_[4], _[6], cnt)])
            except Exception as e:
                print_queue.put([self.name, str(e)])
            time.sleep(5)

class wa(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.ht = Http()
    def run(self):
        global cnt
        while True:
            try:
                _ = self.ht.request('http://page.vote.qq.com/survey.php?PjtID=1327749&SubjID=1363334&OptID=100790&fmt=json&result=0&rdm=' + rnd(),
                    headers= {"Accept":"*/*",
                        "Accept-Encoding":"gzip,deflate",
                        "Accept-Language":"zh-CN",
                        "Connection":"keep-alive",
                        "DNT":"1",
                        "Host":"page.vote.qq.com",
                        "Referer":"http://hb.qq.com/a/20110805/000892.htm",
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.1.2000 Chrome/30.0.1599.101 Safari/537.36"
                })
                if 'page.vote.qq.com' in _[1]:
                    print_queue.put([self.name, 'wait'])
                    time.sleep(random.random()*10 + 5)
                    continue
                print_queue.put([self.name, ','.join([_[0]['status'], _[1].split(':')[1].split(',')[0]])])
                cnt += 1
            except Exception as e:
                print_queue.put([self.name, str(e)])
            time.sleep(random.random()*2)
            
            
class prt(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        while True:
            try:
                print(':'.join(print_queue.get(False)))
            except Empty:
                time.sleep(1)
lst = []
_ = prt()
_.start()
lst.append(_)
_ = wo('cnt')
_.start()
lst.append(_)
for i in range(100):
    _ = wa('vote-%d' % i)
    lst.append(_)
    _.start()
    time.sleep(random.random()*5)

for t in lst:
    _.join()
