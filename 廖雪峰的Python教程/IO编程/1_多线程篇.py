# =======================================================
# ============= mutiprocessing 多进程
# =======================================================
from multiprocessing import Process
import os

# 字进程需要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

def fun1():
    if __name__ == '__main__':
        print('Parent process %s.' % os.getpid())
        p = Process(target=run_proc, args=('test',))
        print('Child process will start.')
        p.start()
        p.join()
        print('Child process end.')

# =======================================================
# ============= pool 进程池
# =======================================================
from multiprocessing import Pool
import time,random

# 字进程需要执行的代码
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random()* 3)
    end = time.time()
    print('Task %s runs %0.2f second.' % (name, (end - start)))

def fun2():
    if __name__ == '__main__':
        print('Parent process %s.' % os.getpid())
        pool = Pool(10)
        for i in range(8):
            pool.apply_async(long_time_task, args=(i,))
        print('Waiting for all subprocesses done...')
        pool.close()
        pool.join()
        print('All subprocesses done.')

# =======================================================
# ============= communicate on threads 进程间的通信
# =======================================================
from multiprocessing import Queue

# 进程间写数据
def process_write(q):
    print('Process to write: %s...' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

def process_read(q):
    print('Process to read : %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

def fun3():
    if __name__ == '__main__':
        # 父进程创建Queue,并传给各个子进程
        q = Queue()
        pw = Process(target=process_write, args=(q,))
        pr = Process(target=process_read, args=(q,))
        # 启动子进程pw,写入
        pw.start()
        # 启动子进程pr,读取
        pr.start()
        # 等待pw结束
        pw.join()
        # pr进程是死循环，无法等待其结束，只能强制终止
        pr.terminate()

# =======================================================
# ============= thread demo 线程例子
# =======================================================
import threading

# 新线程执行的代码
def thread_loop():
    print('Thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n+ 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)


def fun4_thread_demo():
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=thread_loop, name='LoopThread', args=())
    t.start()
    # t.join()
    print('Thread %s ended.' % threading.current_thread().name)


# =======================================================
# ============= mutithread motify value demo 多线程修改值，导致值乱了的问题
# =======================================================
# 假定这是你的银行存款
balance = 0
# 新线程执行的代码
def change_it(n):
    # 先存后取，结果应该为0
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(1000000):
        change_it(n)

lock = threading.Lock()
def run_thread_with_lock(n):
    for i in range(1000000):
        # 先获取锁
        lock.acquire()
        try:
            # 放心改吧
            change_it(n)
        finally:
            # 释放锁
            lock.release()

def fun5_mutithread_demo():
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=run_thread_with_lock, name='LoopThread', args=(5,))
    t2 = threading.Thread(target=run_thread_with_lock, name='LoopThread2', args=(8,))
    t.start()
    t2.start()
    t.join()
    t2.join()
    print('Thread %s ended.' % threading.current_thread().name)
    # 循环次数达到100w才会出现
    print('Balance is %s.' % balance)

# =======================================================
# ============= LocalThread
# =======================================================
# 创建全局ThreadLocal对象
local_school = threading.local()
# 新线程执行的代码
def process_student():
    # 获取当前线程关联的student
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的Student
    local_school.student = name
    process_student()


def fun6_thread_local():
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=process_thread, name='LoopThread', args=('Alice',))
    t2 = threading.Thread(target=process_thread, name='LoopThread2', args=('Bob',))
    t.start()
    t2.start()
    t.join()
    t2.join()
    print('Thread %s ended.' % threading.current_thread().name)

# fun1()
# fun2()
# fun3()
# fun4_thread_demo()
# fun5_mutithread_demo()
fun6_thread_local()