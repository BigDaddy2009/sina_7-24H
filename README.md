# 新浪财经7*24H直播

#### url地址：
http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery111205681467546222541_1577012645246&page=1&page_size=20&zhibo_id=152&tag_id=10&dire=f&dpc=1&pagesize=20&id=1542238&type=0&_=1577012645269

http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery111205681467546222541_1577012645246&page=1&page_size=20&zhibo_id=152&tag_id=10&dire=f&dpc=1&pagesize=20&id=1542238&type=0&_=1577012645267

#### ID表
全部
A股
宏观
行业
公司
数据
市场
观点
央行
其他
#### 其他参数
page
page_size：做大值可能为50，200的话会进行除法运算后再返回结果
zhibo_id
tag_id
dire
dpc
pagesize
type：0为id往后排，1为id往前排
时间戳：时间戳在这里没有意义，可能只起到验证的作用

#### 返回的responce的处理
requests库get到的结果为str，需要去头去尾，然后得到一个json格式的str，然后对其进行转换为字典格式，提取字典中的字段["result"]['data']['feed']['list']
然后再对其进行遍历['rich_text']
可以得到文章标题
#### def 方法
1 获取历史数据
先获取最新的新闻ID
设置type=1，逐步往前遍历
进行存储
2 获取最新的新闻
查看最新获取的新闻有没有在新闻list中，不在的话为新的新闻
