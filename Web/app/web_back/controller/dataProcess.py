from _weakref import proxy
from flask import request
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from pip._vendor.progress import counter
from web_back.model.models import upload_img, imgs, information
from web_back.common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from web_back.common.exts import db
import tqdm
import threading
import time
#coding=utf-8
import json
import os

SEPARATOR="<SEPARATOR>"#分隔符
#RecThread为线程类主要用于控制线程的创建和限制创建线程的上限，设置最大并发线程数为100，超过100后的线程就会处于等待状态，直到线程列表移除一个线程才可以就行


class RecThread(threading.Thread):
    tlist = []  # 用来存储队列的线程
    maxthreads = 100  # 最大并发线程数
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
class ReciveData:
    def __init__(self):
        pass

    def runThread(self):
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
        user_phone = request.form.get('userPhone')
        user_name = request.form.get('userName')
        # t = request.form.get('uploadTime')
        t = '2021'
        desc = request.form.get('imageDesc')
        theme = request.form.get('imageTitle')
        number =request.form.get('imageCount')

        user = wx_user.query.filter(wx_user.phone == user_phone).first()  #获取用户名
        user_id = user.id  #获取用户ID
        print(user_id)
        number = int(number)
        d=Data_deal(user_id,number,desc,theme)
        d.update_info()   
        threadPool = ThreadPoolExecutor(max_workers=number, thread_name_prefix="pro")  # 根据用户上传的文件
        # 一个用户来访问就会开一个线程，然后根据他传过来的图片数量，开启线程池读取文件
        for i in range(number):
            future = threadPool.submit(self.re(user_name, user_id, t))  # j将线程提交到线程池
        threadPool.shutdown()
        #返回信息给客户端图片接收完毕
        for j in r.scan_iter('imgs*'):
            r.delete(j)
        for k in r.scan_iter('upload_img*'):
            r.delete(k)  
                
    def re(self, username,user_id, t):
        t0 = time.time()
        basepath=os.path.split(os.path.dirname(__file__))[0]
        image = request.files.getlist('photo')
        for i in range(len(image)):  # 循环接收文件
            file_format= 'jpeg'
            filename = image[i].filename  # 获取带扩招名的文件名
            file_size = 10240
            print(f"文件名：{filename}<-------->")
            if file_format == ".txt":
                dire = "data/" 
                
            else:
                dire = "images/"

            file_path = Path(os.path.join(basepath, "static/"+ dire + username))  # 根据用户名创建文件夹
            base_path = Path(os.path.join(basepath,"static/"+ dire + username + "/" + t))   # 根据每次上传文件的时间戳创建文件夹
            if file_path.exists():  # 判断以用户名命名的文件夹是否存在
                if base_path.exists():  # 当以用户名命名的文件夹存在，则判断以当前获取的时间戳命名的文件夹是否存在
                    if os.path.exists(filename):  # 判断发送的文件是否已经存在
                        # self.send(f"文件{filename}已经存在！")   
                        break                                            
                    else:
                        file_name = "static/"+ dire + username + "/" + t + "/" + filename
                        filename = os.path.join(basepath, "static/"+ dire + username + "/" + t + "/" + filename)  #路径拼接
                        # 设置图片的真实存储路径
                else:  # 如果以用户名命名的文件存在，但不存在以当前获取的时间戳命名的文件夹,
                        #则为创建文件夹，并为其创建一个获取的时间戳的文件夹，用于存放其发送到服务器的图片 
                    os.mkdir(base_path)
                    file_name = "static/"+ dire + username + "/" + t + "/" + filename
                    filename = os.path.join(basepath, "static/"+ dire + username + "/" + t + "/" + filename)  #路径拼接
            else:  # 如果以用户名命名的文件夹不存在，则说明压根没登录过则为其创建一个以用户命名的文件夹，
                # 并将获取其传输过来的时间戳为其创建一个文件用于存放本次上传的图片                   
                os.mkdir(file_path)
                os.mkdir(base_path)
                file_name = "static/"+ dire + username + "/" + t + "/" + filename                  
                filename = os.path.join(basepath, "static/"+ dire + username + "/" + t + "/" + filename)  #路径拼接
            image[i].save(filename)
            # # if Path(filename).exists():  # 判断发送的文件是否已经存在
            # #     local_size = os.path.getsize(filename)
            # #     if local_size != file_size:
            # #         # self.send(f"文件{filename}已经存在！")
          
                            
            # if flag == False:  # 一个文件已经接受完毕，退出循环读取但并没有退出最外层循
            #     print("数据处理")
            #     if file_format == ".txt":
            #         upoload = upload_img.query.filter(
            #             upload_img.user_id == user_id).order_by(upload_img.date.desc()).first()  # 获取刚刚上传图片数据的id
            #         image_id = upoload.id  # 获取当前上传用户的id
            #         file_name = '\'%s\'' % file_name
            #         sql='update imgs set data_path=%s where upload_id=%s' %(file_name,image_id)
            #         cursor.execute(sql)
            #         database.commit()
            #     else:
            #         upoload = upload_img.query.filter(
            #             upload_img.user_id == user_id).order_by(upload_img.date.desc()).first()  # 获取刚刚上传图片数据的id
            #         image_id = upoload.id  # 获取当前上传用户的id
            #         img = imgs(upload_id=image_id, file_path=file_name, data_path=0)
            #         db.session.add(img)
            #         db.session.commit()
            #     break
 

class Data_deal():
    def __init__(self,user_id,number,desc,theme):
        self.user_id=user_id
        self.number=number
        self.desc=desc
        self.theme=theme

    def update_info(self):
        upload_data = upload_img(user_id= self.user_id, number=self.number,equip_id=0,
            image_desc=self.desc, image_title=self.theme)  # 将当前登录用户的id作为upload_img的user_id
        db.session.add(upload_data)
        db.session.commit()
        # r.delete('eqimfo'+str(self.equip_id))
        upoload = upload_img.query.filter(
            upload_img.user_id == self.user_id).order_by(upload_img.date.desc()).first()  # 获取刚刚上传图片数据的id
        image_id = upoload.id  # 获取当前上传用户的id


        sql='select id from wx_user'#查询所有用户的id
        cursor.execute(sql)#执行SQL语句
        alluser_id=cursor.fetchall()#获取所有用户的id

        # 使用for/in循环对所有用户添加未读数据
        for (i,) in alluser_id:
            if (i == self.user_id):
                continue

            info_data = information(user_id=i, image_id=image_id, equip_id=self.equip_id)  # 设备equip_id目前手动设置
            db.session.add(info_data)
            db.session.commit()