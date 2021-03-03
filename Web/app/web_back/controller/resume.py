from _weakref import proxy
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from pip._vendor.progress import counter
from common.exts import db
from common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from model.models import upload_img, imgs, information
import tqdm
import threading
import time
#coding=utf-8
import json
import os
import time


SEPARATOR="<SEPARATOR>"#分隔符
#RecThread为线程类主要用于控制线程的创建和限制创建线程的上限，设置最大并发线程数为100，超过100后的线程就会处于等待状态，直到线程列表移除一个线程才可以就行


class RecThread(threading.Thread):
    tlist = []  # 用来存储队列的线程
    maxthreads = 50  # 最大并发线程数
    event = threading.Event()  # 用事件来让超过最大线程设置的并发程序等待
    lock = threading.Lock()  # 线程锁

    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target  # run方法中执行的操作

    def run(self):
        try:
            self.target()
        except:
            print("接收完毕线程关闭")
        RecThread.lock.acquire()  # 获得线程锁
        RecThread.tlist.remove(self)  # 将线程从线程队列移除
        # 如果移除此完成的队列线程数刚好达到99，则说明有线程在等待执行，那么我们释放event，让等待事件执行
        if len(RecThread.tlist) == RecThread.maxthreads - 1:
            RecThread.event.set()  # 让等待的线程执行
            RecThread.event.clear()
        RecThread.lock.release()  # 释放线程锁

    def newthread(proxy, counter, target):  # 创建新线程
        RecThread.lock.acquire()  # 获得线程锁
        sc = RecThread(target)  # 创建线程类
        RecThread.tlist.append(sc)  # 将新建的线程加入线程队列
        RecThread.lock.release()  # 释放线程锁
        sc.start()  # 开启线程

    # 将新线程方法定义为静态变量，供调用
    newthread = staticmethod(newthread)


# 数据接收类
class ResumeData:
    def __init__(self, ws):
        self.ws = ws

    def runResume(self):
        RecThread.lock.acquire()
        if len(RecThread.tlist) >= RecThread.maxthreads:
            # 如果目前线程队列超过了设定的上线则等待。
            RecThread.lock.release()
            RecThread.event.wait()  # scanner.event.set()遇到set事件则等待结束
        else:
            RecThread.lock.release()
        RecThread.newthread(proxy, counter, target=self.ctreate_ThreadPool())

        for t in RecThread.tlist:
            t.join()  # j 待线程的执行完成才继续

    def ctreate_ThreadPool(self):
        recived = self.ws.receive()
        if not recived is None:
            # global user_id
            rec = str(recived, encoding="utf8")
            username, t, number = rec.split(SEPARATOR)
                  
            # 接收传过来的用户名，设备id，时间戳，，图片数量，主题，描述
            number = int(number)  # 将number转为int型                      
            threadPool = ThreadPoolExecutor(max_workers=number, thread_name_prefix="pro")  # 根据用户上传的文件
            # 一个用户来访问就会开一个线程，然后根据他传过来的图片数量，开启线程池读取文件
            for i in range(number):
                future = threadPool.submit(self.re(username, t))  # j将线程提交到线程池
            threadPool.shutdown()
            
            print("接收完毕")
            #返回信息给客户端图片接收完毕


    def re(self, username,t):
        count = 0
        flag = False  # 循环读取的标识
        t0 = time.time()
        while 1:  # 循环接收文件
            length = 0  # 已接受文件长度
            if count == 0:  # count说明传过来的是一个文件的文件名文件大小等信息
                recived = self.ws.receive()  # 接收信息
                if recived == None:  # 当接收到的数据为空说明没有传输过的文件，退出循环读取文件
                    print("目前用户还没有发送信息请等候：")
                    break
                rec = str(recived, encoding="utf8")
                self.ws.send("0")
                filename, file_size, file_format= rec.split(SEPARATOR)
                # 根据分隔符分割各传过来的信息，即获取文件名，文件大小，用户名，设备ID
                # print(f"文件名：{filename}<-->文件大小：{file_size}<-->时间戳：{t}")
                filename = filename.split("/")[-1]  # 获取带扩招名的文件名
                file_size = int(file_size)
                if file_format == ".txt":
                    dire = "data/" 
                    
                else:
                    dire = "images/"

                file_path = "project/web_back/static/"+ dire + username + "/" + t + "/" + filename  # 根据用户名创建文件夹
                

            pro = tqdm.tqdm(range(file_size), f"接收续传文件{filename}", unit="B", unit_divisor=1024)  # 设置进度调条
            with open(file_path, "ab") as f:  # 写文件
                print("续传文件")
                for _ in pro:  # 根据进度条读取数据，即每次读取1024B的数据
                    bytes_read = self.ws.receive()
                    print(bytes_read)
                    if bytes_read == None:
                        flag = True
                        print("第二次死了")
                        self.ws.close()
                        break
                    f.write(bytes_read)
                    pro.update(len(bytes_read))  # 更新进度条
                    count += 1  # 当count不为零说明开始接收文件内容
                    length += len(bytes_read)  # 已经读取的多少长度的文件
                    file_name = "static/"+ dire + username + "/" + t + "/" + filename 
                    self.ws.send(f"{length}")
                    print(f"第二次接收了{length}字节------------",f"大小为{file_size}字节")
                    if length == file_size:  # 文件还没接收完
                        self.ws.send(f"{length}")
                        print("第二次正常")
                        flag = True
                        break #退出for循环但没有退出with的循环读取
                print("with_2")                   
           
            
