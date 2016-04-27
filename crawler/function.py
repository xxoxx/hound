# -*- coding=utf-8 -*-
import re,sys;
from urlparse import urlparse
sys.path.append("..")
from mysql.DB import DB;
"""
URL: print list(urlparse("http://www.baidu.com/s/index.php?id=1&name=liu#111"))
[0] == scheme -> scheme='http',
[1] == netloc -> netloc='www.baidu.com',
[2] == path -> path='/s/index.php'',
[3] == params -> params='',
[4] == query -> query='id=1&name=liu',
[5] == fragment ->fragment='111'
"""
def handle(url,dangqian_url,tables,domain):
	
	url_2 = urlparse(url);
	url = url.replace('http://','').replace('https://','');
	
	if url_2.netloc != "":  #判断是否有netloc；
		
		if re.search(".%s" % (domain) ,url_2.netloc) != None: #如果相关域名存在的话
			print '\033[1;38;1m  Get a 1 related domain name  %s \033[0m' % (url.split('/')[0]);
			strinfo = re.compile("_p$")
			tables = strinfo.sub('',tables)
			

			try:
				ip = socket.gethostbyname(url);
			except Exception,e:
				ip = False;
			if ip:
				DB().Domain_storage(tables,url.split('/')[0],ip);   #url.split('/')[0]   split('/')[0]  意思是从第一个/ 开始删除 比如 baidu.com/s/w/1.asp 删除后就成了 baidu.com
			
			return False;
	elif re.search("^/",url_2.path)!= None: #如果一开始是/的话 那么他就会跳转到根目录的
		sql = 'select count(*) from php90_cn_p where url like "%'+ url_2.path+'%"';
		if DB().query(sql) > 100 :
			return False;
		else:

			return domain+url_2.path+url_2.query;

		#不能删 提醒自己
	elif re.search("^./",url_2.path) != None:
		sql = 'select count(*) from php90_cn_p where url like "%'+ url_2.path+'%"';
		if DB().query(sql) > 100 :
			return False;
		else:
			if len(dangqian_url.split('/')) > 1 :
				dangqian_url2 = dangqian_url.split('/')[-1]
				strinfo = re.compile("%s$" % (dangqian_url2))
				dangqian_url = strinfo.sub('',dangqian_url) #把 最后一个 / 后面内容删掉
				return dangqian_url+url_2.path.replace("./","/")+url_2.query;
			else:
				return dangqian_url+url_2.path.replace("./","/")+url_2.query;
	else:
		sql = 'select count(*) from php90_cn_p where url like "%'+ url_2.path+'%"';
		if DB().query(sql) > 100 :
			return False;
		else:
			if len(dangqian_url.split('/')) > 1 :
				dangqian_url2 = dangqian_url.split('/')[-1]
				strinfo = re.compile("%s$" % (dangqian_url2))
				dangqian_url = strinfo.sub('',dangqian_url) #把 最后一个 / 后面内容删掉
				return dangqian_url+url_2.path+url_2.query;
			else:
				return dangqian_url+url_2.path.replace("./","/")+url_2.query;
		

	
	

		
		





