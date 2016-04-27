# -*- coding=utf-8 -*-
import requests,re,sys,time,threading,socket;
sys.path.append("..")
from mysql.DB import DB;

db_plus = DB();
class simple(object):
	
	walk = 0;
	walk2 = 0;
	recursion_walk=0
	"""简单的http请求"""
	def __init__(self):
		self.header2 = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection':'keep-alive',
		'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'};
	def h_get_text(self,url): #获取源码
		try:
			r = requests.get(url,headers=self.header2,timeout=10);  
			return r.text.encode('utf-8'); 
		except Exception,e:
			print'\033[1;31;1m'+"Exception: %s  Error: %s " % (Exception,e) +'\033[0m';
			return '';

	def h_post_text(self,url,canshu): #获取源码
		try:
			r = requests.post(url,headers=self.header2,data=canshu,timeout=7);  

			return r.text.encode('utf-8'); 
		except Exception,e:
			#print'\033[1;31;40m'+"Exception: %s  Error: %s " % (Exception,e) +'\033[0m';
			return '';

	def h_get_isurl(self,tables,url): #接口获取到的域名 然后判断域名是否存在 如果存在就如裤
		try:
			r = requests.get(url,headers=self.header2,timeout=5);  
			isurl_html = r.text.encode('utf-8'); #获取源码
			
			r = 'window.location="http://search.114so.cn/+';
			if re.search(r,isurl_html) == None and re.search("<title>Access forbidden!</title>",isurl_html) == None: #如果域名存在的话
				ip = socket.gethostbyname(url.replace('http://',''));
				db_plus.Domain_storage(tables.replace('.','_'),url.replace('http://',''),ip); #入裤
				print '\033[1;33;1m   Successful storage  ^_^. \033[0m';
		except Exception,e:
			return False;
			

	def h_get_for_isurl(self,tables,url): #接口获取到的域名 然后判断域名是否存在 如果存在就如裤
		try:
			r = requests.get(url,headers=self.header2,timeout=5);  
			isurl_html = r.text.encode('utf-8'); #获取源码
			r = 'window.location="http://search.114so.cn/+';
			if re.search(r,isurl_html) == None and re.search("<title>Access forbidden!</title>",isurl_html) == None: #如果域名存在的话
				ip = socket.gethostbyname(url.replace('http://',''));
				db_plus.Domain_storage(tables.replace('.','_'),url.replace('http://',''),ip); #入裤
				print '\033[1;33;1m   Successful storage  ^_^. \033[0m';
		except Exception,e:
			return False;









##########################循环判断域名是否存在   如果存在就入库#####################
						#		url，字典
	def h_get_blast_text(self,url,lis): #循环判断域名是否存在   如果存在就入库

		this = simple();
		for x in range(len(lis)):
			h_url = lis[x][0]+"."+url;

			this.is_url(h_url,url)
			time.sleep(4);

	def is_url(self,url,tables):
		try:
			ip = socket.gethostbyname(url);
			simple.walk = simple.walk +1;
			
		except Exception,e: #请求超时 说明没有
			simple.walk = simple.walk +1;
			ip = False;
		if ip: #如果域名存在的话
			
			url2 = url.replace('http://','');
			tables = tables.replace('.','_');
			db_plus.Domain_storage(tables,url2,ip); #入裤


###########################################################################























##########################递归 循环判断域名是否存在   如果存在就入库#####################
	def recursion_h_get_blast_text(self,url,lis,tables): #循环判断域名是否存在   如果存在就入库
		this = simple();
		
		for x in range(len(lis)):

			h_url = lis[x][0]+"."+url;
			this.recursion_is_url(h_url,tables);

			time.sleep(4);
			
			
		# for tt in a:
		#    	tt.join(); #等待所有线程结束

	def recursion_is_url(self,url,tables):
		
		try:			
			ip = socket.gethostbyname(url);
			simple.walk2 = simple.walk2 +1;
			
		except Exception,e: #请求超时 说明没有
			simple.walk2 = simple.walk2 +1;
			ip = False;
		
		if ip: #如果域名存在的话
			
			url2 = url.replace('http://','');
			db_plus.Domain_storage(tables,url2,ip); #入裤

		



###########################################################################

	

