#coding:utf-8
from httplib2 import Http
import re
import time
today = time.strftime('%Y-%m-%d 00:00:00',time.localtime(time.time()))
ticket = "1Z7F382V0319072001"
a,b = Http("Z:\TEMP").request("http://tr.4px.com/Transport/LogisticsTransferTrace.aspx?code=%s" % ticket,
    headers = {"Referer":"http://tr.4px.com/Transport/TransportInfo.aspx",
                 "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"gzip,deflate",
                "User-Agent":"Mozilla/5.0"})
lines = re.findall('<span class="pad_right">([\d\s\-:]+)</span>([^\/]+)</span>', b)
print(("【4px物流查询工具】\n运  单  号：%s\n物流轨迹:" % ticket).decode('utf-8'))
print('\n'.join(map(lambda x: ' '.join(x) + (' NEW' if x[0] > today else ''), lines)).decode('utf-8'))