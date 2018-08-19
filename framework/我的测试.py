
if __name__ == '__main__':


    # 测试setup.py中的技术
    # 每次读文件中一行数据
    # for line in open('setup.py', encoding='utf8'):
    #     print(line)
    # []是一个列表生成式, () 获取一个生成器对象
    # lineitr = (line.strip() for line in open('setup.py', encoding='utf8'))
    # # print(lineitr) # <generator object <genexpr> at 0x106cae518>
    # lines = [line for line in lineitr if line and not line.startswith("#")]
    # for line in lines:
    #     print(line)
    #
    # from os.path import dirname, join
    # # 打印当前文件的目录
    # print(dirname(__file__))
    # # join拼接路径
    # print(join(dirname(__file__),'VERSION.txt'))

    # 测试日志
    import logging

    # 日志等级
    # logging.DEBUG 调试
    # logging.INFO  信息, 程序运行的状态信息
    # logging.WARNING 警告, 程序没有报错, 但是不建议这么使用
    # logging.ERROR   错误   程序错误
    # logging.CRITICAL 严重错误  程序挂掉的严重错误.

    # 设置日志等级
    logging.basicConfig(level=logging.WARNING)

    logging.debug('调试日志')
    logging.info('运行状态描述信息')
    logging.warning('警告')
    logging.error('错误')
    logging.critical('严重错误')


    try:
        # 记录错误日志
        raise Exception('异常啦!')
    except Exception as ex:
        # exception在except中使用, 才会有报错位置信息
        logging.exception(ex)