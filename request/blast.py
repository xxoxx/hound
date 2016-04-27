# -*- coding=utf-8 -*-
import threading,sys,time;
sys.path.append("..")
from mysql.DB import DB;
from request.simple import simple 
class blast(simple):
	xiancheng = [];
	"""爆破域名"""
	def blast_url(self,url,t,lis):
		progress = sys.stdout;
		#lis = DB().query_all("select lis from lis"); #字典数据
		total = len(lis) #获取字典总数
		blast_i = []; #获取线程是否结束
		fenliang = total / t;  #总数除以线程 得到每份数量
		kaishi = 0;
		jiewei = fenliang;
		self.simple = simple();
		print '\033[1;36;1m Is finishing the dictionary, ready to send all requests \r \033[0m'
		while True:
			list2 = lis[kaishi:jiewei]; #获取成员份量
			t = threading.Thread(target=self.simple.h_get_blast_text,args=[url,list2]); #判断是否存在域名 如果有就入库 表名是url的值
			t.start();
			blast_i.append(t)
			
			if jiewei > total:
				break;

			kaishi = kaishi + fenliang;
			jiewei = jiewei + fenliang;
			time.sleep(0.02);
		
		print '\033[1;36;1m All requests are sent, waiting for a response. √ \r \033[0m'
		
		inhour = 7; 
		for x in xrange(7):

			progress.write('\033[1;36;1m Still need to wait %i \r \033[0m' % inhour);
			progress.flush();
			inhour = inhour - 1;
			time.sleep(1);
		print '\r \n';
		print '\033[1;36;1m Need a little time ..... \r\n \033[0m'
		print '\n '
		while True:
			
			progress.write("\033[1;32;1m mm^mdomain: %s ----total: %i , ----Already request:%i  \r \033[0m" % (url,total,simple.walk) );
			progress.flush();
			if simple.walk+80 >= total:
				print ' \n \n Send request: %i' % (total)
				print '\n Wait for all requests to end! '
				break;
			time.sleep(0.2);
		
		for tt in blast_i:
 	   		tt.join(); #等待所有线程结束
 	   	print '\r \n'
 	   	print '\033[1;36;1m oK,Sorting data √ \033[0m';





 	   	#递归爆破				#表名 线程 字典  批量域名
	def recursion_blast_url(self,tables,t,lis,url_list):
		progress = sys.stdout;
		tables = tables.replace('.','_');
		total = len(lis); #请求总数

		
		fenliang = total / t;  #总数除以线程 得到每份数量
		
		kaishi = 0;
		jiewei = fenliang;
		
		self.simple = simple();
		
		for recursion_url in url_list:
			print " URL:"+recursion_url[0]+"-->\033[1;32;1m  Send out all the requests \r \033[0m"
			while True:
				list2 = lis[kaishi:jiewei]; #获取成员份量
				
				t = threading.Thread(target=self.simple.recursion_h_get_blast_text,args=[recursion_url[0],list2,tables]); #判断是否存在域名 如果有就入库 表名是url的值
				t.start();
				blast.xiancheng.append(t);
				if jiewei > total:
					kaishi = 0;
					jiewei = fenliang
					break;
				else:
					kaishi = kaishi + fenliang;
					jiewei = jiewei + fenliang;
				time.sleep(0.02);
			sql = "update %s set recursion = 1 where url = '%s'" % (tables,recursion_url[0]);
			DB().increase(sql);
		
		for tt in blast.xiancheng:
		   	tt.join(); #等待所有线程结束

		print "\033[1;32;1m  Above the domain name to send complete 0o(^_^)o0\r \033[0m   <--"

