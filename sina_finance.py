import requests
import json
import time
import pandas as pd
from snownlp import SnowNLP

#url = 'http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery111205681467546222541_1577012645246&page=1\
#	&page_size=50&zhibo_id=152&tag_id=10&dire=f&dpc=1&pagesize=20&id=1542479&type=1&_=1577021071472'
def get_html_info(url):
	html = requests.get(url)
	content = html.content[46:-14].decode("utf8")
	# 这里将str类型的content转换成了dict类型的
	content = json.loads(content)
	df = pd.DataFrame(columns = ['id','rich_text','create_time','tag'])
	#df.columns = ['id','rich_text','create_time']
	for i in content["result"]['data']['feed']['list']:
	#print(i)#i的格式为字典
		need_option=['id','rich_text','create_time','tag']#定义需求关键词
		for listkey in list(i.keys()):#字典在遍历的时候不能修改元素，此处先编程列表在变回字典
			if listkey not in need_option:
				i.pop(listkey)#pop用于删除无用的key
		#print(i['tag'])
		tag = ''
		for j in i['tag']:
			tag = tag+'&'+j['name']
		new_df = pd.DataFrame(columns = ['id','rich_text','create_time','tag'])
		new_df.loc[0] = [i['id'],i['rich_text'],i['create_time'],tag]
		df = df.append(new_df)
	df.reset_index(inplace = True, drop=True)
	#print(df)
	return df
	#print(round(time.time()*1000))
	#exit()
def get_url(id,type):
	if id == 0:
		url = 'http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery111205681467546222541_1577012645246&page=1\
			&page_size=100&zhibo_id=152&tag_id=10&dire=f&dpc=1&pagesize=20&type=%s&_=%s'%(type,round(time.time()*1000))
	else:
		url = 'http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery111205681467546222541_1577012645246&page=1\
			&page_size=100&zhibo_id=152&tag_id=10&dire=f&dpc=1&pagesize=20&id=%s&type=%s&_=%s'%(id,type,round(time.time()*1000))
	return url
def get_new_news(new_df):
	url = get_url(0,0)
	#获取最新的新闻列表
	df = get_html_info(url)
	print('原有新闻列表的ID:'+str(max(new_df.id)))
	for i in df.index:
		print('获取的新的ID：'+str(df.at[i,'id']))
		#print(i < max(new_df.id))
		if df.at[i,'id'] <= max(new_df.id):
			print('未发现新的ID,不需要进行处理')
			return new_df
		else:
			print('发现了新的ID，进行插入操作')
			print(df.loc[0])
			new_df = new_df.append(df.loc[0])
			new_df.reset_index(inplace = True, drop=True)		
	return new_df
def get_news():
	url = get_url(0,0)
	df = get_html_info(url)
	new_id = df.at[99,'id']
	for i in range(1):
		#print(new_id)
		url_a = get_url(new_id,1)
		df_a = get_html_info(url_a) 
		new_id = df_a.at[99,'id']
		df = df.append(df_a)
		#print(new_id)
	df.reset_index(inplace = True,drop = True)
	df['snownlp_score'] = ''
	for i in df.index:
		#print(df.at[i,'rich_text'])
		s = SnowNLP(df.at[i,'rich_text'])
		#print(s.sentiments)
		#exit()
		df.at[i,'snownlp_score'] = round(s.sentiments,2)    
	#df.to_excel('7×24H直播.xlsx')
	return df
if __name__ == '__main__':
	df = pd.DataFrame()
	while True:
		if df.empty:
			df = get_news()#获取历史新闻
		df = get_new_news(df)#根据历史新闻的最新的id进行比较，并进行插入
		print('0.5min后刷新--------------------------')
		time.sleep(30)

