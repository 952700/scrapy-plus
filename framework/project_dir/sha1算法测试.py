import hashlib
import six



s = 'http://www.baidu.com'

# 1. 获取sha1算法对象
sha1 = hashlib.sha1()

# 2. 更新sha1算法对象中的数据
# upate中只支持二进制数据, 不支持字符串
sha1.update(s.encode())

# 3. 获取该数据对应的指纹(消息摘要); 也就是一个十六进制的指纹
fp = sha1.hexdigest()
print(fp)

# 关于py2和py3中的字符串
# py3中字符串默认是str, str就是一个unicode的字符串
# py2中字符串str是二进制数据, 编码后是unicode烈性

def get_bytes_from_str(s):
    if six.PY3:
        # 如果是py3, 如果是str类型就需要进行编码
        if isinstance(s, str):
            return s.encode('utf8')
        else:
            return s
    else:
        # 如果是py2, 如果是str类型就直接返回
        if isinstance(s, str):
            return s
        else:
            # 在py2中encode默认使用ascii码进行编码的,此处不能省
            return s.encode('utf8')

