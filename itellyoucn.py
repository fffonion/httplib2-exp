import json
import httplib2
import re
import _headers
ht = httplib2.Http('itellyou')
rsp, ct = ht.request('http://msdn.itellyou.cn/', headers=_headers.get())
lists = re.findall('\#collapse_([0-9a-z-]+)\"\>([^\<]+)\<', ct)
hpost = dict(_headers.get())
hpost.update({
    'Origin': 'http://msdn.itellyou.cn',
    'Referer': 'http://msdn.itellyou.cn/',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
resfile = open('itellyou_links.txt', 'w')


def p_w(s, nowrite=False):
    print(s)
    if not nowrite:
        resfile.write(('%s\n' % s).encode('utf-8'))

for (gid, name) in lists:
    p_w('[%s]' % name.decode('utf-8'))
    ct = ht.request('http://msdn.itellyou.cn/Category/Index', method='POST', body='id=%s' % gid, headers=hpost)[1]
    res_dict = json.loads(ct)
    for dic in res_dict:
        p_w('-%s' % dic['name'], nowrite=True)
        ct = ht.request('http://msdn.itellyou.cn/Category/GetLang', method='POST', body='id=%s' % dic['id'], headers=hpost)[1]
        lang_ids = json.loads(ct)['result']
        for lang in lang_ids:
            p_w('--%s' % lang['lang'], nowrite=True)
            ct = ht.request(
                'http://msdn.itellyou.cn/Category/GetList', method='POST', 
                body='id=%s&lang=%s&filter=true' % (dic['id'], lang['id']), headers=hpost)[1]
            link_ids = json.loads(ct)['result']
            for link in link_ids:
                p_w(link['name'])
                p_w(link['url'])
    resfile.flush()
resfile.close()
