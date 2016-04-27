#encoding=utf-8
import sys,requests,re,time,threading;
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup
from function import handle
sys.path.append("..")
from core import CORE;
from mysql.DB import DB;

class crawler(object):
	"""爬虫"""
	
	crawler_progress = []; #爬虫进展
	header3 = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection':'keep-alive',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'};
						#表名 网站 线程 爬虫深度
	def __init__(self,table,url,thread,depth): #创建表
		dangqiangurl = url
		print dangqiangurl,'----->Being crawler ! ^_^';
		depth = int(depth);
		thread = int(thread);
		tables = table+"_p";
		domain = url;
		
		sql = "select count(table_name) from information_schema.tables where table_name = '%s' and TABLE_SCHEMA = '%s'" % (tables,CORE.db)	
		
		if not DB().query(sql): #判断表名存不存在 如果不存在就创建
			sql = """CREATE TABLE IF NOT EXISTS %s (
				id int not null primary key auto_increment,
				url text not null comment 'url',
				domain text not null comment 'yuming',
				state int default 0)DEFAULT CHARSET=utf8""" % (tables);
			
			
			DB().increase(sql); #创建表名

		DB().p_url_increase(tables,url,domain); #入裤
		
		while True: 
			
			now_depth = DB().query("select count(*) from %s where domain = '%s' and state = 1" % (tables,domain));
			
			if now_depth > depth:
				break;

			now_depth = DB().query("select count(*) from %s where state = 0" % (tables));

			if now_depth == 0:
				break;

			sql = "select url,domain from %s where state = 0 and domain = '%s' limit %i" % (tables,domain,thread);
			
			url = DB().query_all(sql);

			
			if len(url) > 0:
				for x in url: 

					ts = threading.Thread(target=crawler.p_get_text,args=["http://"+x[0],x[0],tables,x[1] ]);
					ts.start();
					crawler.crawler_progress.append(ts) #设置T线程等待结束
					sql = "update %s set state = 1 where url = '%s'" % (tables,x[0])
					DB().increase(sql);
					
					time.sleep(0.2);

				for abcd in crawler.crawler_progress:
					abcd.join();#等待线程结束
					time.sleep(0.5);
					
			else:
				break;
			
		print dangqiangurl,'<----- OK End of crawler  ^_^';
		

	@classmethod
	def p_get_text(cls,url,dangqian_url,tables,domain): #获取源码中的a标签

		try:
			r = requests.get(url,headers=crawler.header3,timeout=5);  
			html_a = r.text.encode('utf-8'); 
			soup = BeautifulSoup(html_a)
			html_a = soup.find_all("a");
		except Exception,e:
			html_a = [];
		if len(html_a) > 0:
			for link in html_a:
				a_href = str(link.get('href'));
				strinfo = re.compile("/+")
				a_href = strinfo.sub('/',a_href) #把 多个 "/" 替换成 / 当然 http:// 变成了http:/了

				strinfo = re.compile("http:/")
				a_href = strinfo.sub('http://',a_href)#将http:/ 变成 http://

				strinfo = re.compile("/+$")
				a_href = strinfo.sub('',a_href) #把最后的 / 删掉

				strinfo = re.compile("#+")
				a_href = strinfo.sub('#',a_href) #把多个# 替换成#
				#print a_href

				if a_href != "/" and a_href != "#" and a_href != "javascript:void(0)" and a_href != "": 
					A = handle(a_href,dangqian_url,tables,domain);
					if A != False and A != None:
						tkk = threading.Thread(target=crawler.if_code,args=[tables,A,domain]);
						tkk.start();
						crawler.crawler_progress.append(tkk)
				
					print a_href,'-->Wait for all responses, and do the two processing ^_^';
				time.sleep(0.2);
			
		else:
			return False;

			
	
			

	@staticmethod
	def if_code(tables,url,domain):
		try:
			
			code=requests.get("http://"+url,timeout=5).status_code

		except Exception,e:
			code = 404
		if code != 404 and code != 403:#如果域名＋ 文件存在
			#入库之前先去除一些杂物
			strinfo = re.compile("/+")
			a_href = strinfo.sub('/',url) #把 多个 "/" 替换成 / 当然 http:// 变成了http:/了
			strinfo = re.compile("http:/")
			a_href = strinfo.sub('http://',url)#将http:/ 变成 http://
			strinfo = re.compile("/+$")
			a_href = strinfo.sub('',url) #把最后的 / 删掉
			
			DB().p_url_increase(tables,a_href,domain); #入裤








