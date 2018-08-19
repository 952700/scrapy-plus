from multiprocessing.dummy import Pool
import time

# 创建线程对象, 如果不指定个数就是你当前CPU的核数
pool = Pool(2)


def task(msg):
    print(msg)


def task_callback_1(temp):
    pool.apply_async(task, args=('线程1', ), callback=task_callback_1)


def task_callback_2(temp):
    pool.apply_async(task, args=('线程2',), callback=task_callback_2)


def task_callback_3(temp):
    pool.apply_async(task, args=('线程3',), callback=task_callback_3)


pool.apply_async(task, args=('线程1', ), callback=task_callback_1)
pool.apply_async(task, args=('线程2', ), callback=task_callback_2)
pool.apply_async(task, args=('线程3', ), callback=task_callback_3)

time.sleep(10)
