#-*-coding:utf-8 -*-
import time,threading,sys;
from  mysql.DB import DB;
from table.tabulate import tabulate
from table.picture import *


def process(fenc,canshu): #导入字典并且还要加载进展条
	output = sys.stdout;
	t = threading.Thread(target=fenc,args=[canshu]); #函数名称
	t.start();
	a = "。";
	while True:
		if t.isAlive():
			x = output.write("\033[5;32;1m Import, may take a few minutes √ %s \r \033[0m" % a);
			output.flush()
			if len(a) > 10:
				a = "。";
				output.flush();
	  			time.sleep(1);
			else:
				a = a+"。";
				output.flush();
	  			time.sleep(1);
  		else:
  			print '                                                                           \r \n ok';
  			break;
  		
  		

def table_print(tables): #表格
	
	a = DB().query_all("desc %s" % (tables));
	table_top = [];

	for x in a:
		table_top.append(x[0])


	b = DB().query_all("select * from %s" % (tables) );


	table_lis = [];
	for x in b:
		table_lis.append(x)


	print tabulate(table_lis, table_top, tablefmt="grid")

