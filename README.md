就……自从知道了httplib2之后抓站什么的基本都用httplib2了

 - urllib2不能通过head指定编码（so不能gzip,要自己做handler）
 
 - 必须手动维护一个连接池才能Connection:keep-alive
 
以上两者（特别是后者）在处理大量请求的时候速度会很慢，而且，不怎么像正常的浏览器~ o(*￣▽￣*)o 

之前用urllib2抓一个壁纸站的时候被IDC花现封ip了，呵呵0.0

另外，官方的httplib2有些缺陷

 - 检查代理的时候没有扫描注册表(urllib, urllib2都是扫描的)
 
 - 没有chunk_read功能，so无法实现下载进度
 
基于以上两点改了个[httplib2plus](https://github.com/fffonion/httplib2-plus)

以上~ ＞▽＜  