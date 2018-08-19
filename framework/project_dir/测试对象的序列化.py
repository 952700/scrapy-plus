from scrapy_plus.http.request import Request
# 实现对象序列化和反序列化
import pickle

# 创建Request对象
request = Request('http://www.baidu.com')

# 序列化: 对象 -> 二进制
data = pickle.dumps(request)
print(data)

# 反序列化: 二进制 -> 对象
req = pickle.loads(data)

print(req)
print(req.url)
