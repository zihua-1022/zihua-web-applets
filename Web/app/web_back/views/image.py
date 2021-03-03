from flask import Blueprint,make_response,request,send_from_directory,render_template,url_for,session,json,flash,redirect,jsonify
from web_back.model.models import imgs,upload_img,wx_user,information
from web_back.common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from web_back.common.exts import db
from datetime import datetime
from pathlib import Path
import os
import time
import tqdm
from PIL import Image
from io import BytesIO
# 实例化一个蓝图
imageapp=Blueprint('image',__name__,template_folder="../templates",static_folder="../static")


# 图片上传
@imageapp.route('/imgs_upload',strict_slashes=True)
def imgs_upload():
    return render_template('imgs_upload.html')

# 数据管理
@imageapp.route('/image_manage',strict_slashes=True)
def image_manage():
    return render_template('imagemanage.html')


@imageapp.route('/wx_pictureContent',methods=['GET', 'POST'],strict_slashes=True)
def wx_pictureContent():
    id=request.values.get('id')
    
   
    sql='select * from upload_img where id=%s' %id
    try:
        cursor.execute(sql)
    except:
        database.ping()
        cursor.execute(sql)

    content=cursor.fetchall()
    json_data = json.dumps(content, cls=CJsonEncoder)
    return json_data

# # 小程序图片上传数量
@imageapp.route('/wx_upload_count', methods=['GET', 'POST'],strict_slashes=True)
def wx_upload_count():
    wxuser=wx_user.query.filter(wx_user.wx_id==openid).first()    #获取用户名

    wxuser_id=wxuser.id     #将用户id当成上传id
    
    img_count=request.values.get('img_count')
    equip_id=request.values.get('equip_id')
    content=request.values.get('content')
    tittle=request.values.get('tittle')
    # upload_data=upload_img(user_id=wxuser.id,number=img_count)#将当前用户的wx_user.id作为upload_img的user_id
    upload_data=upload_img(user_id=wxuser_id,number=img_count,equip_id=equip_id,image_desc=content,image_title=tittle)
    db.session.add(upload_data)
    db.session.commit()

    upoload=upload_img.query.filter(upload_img.user_id==wxuser_id).order_by(upload_img.date.desc()).first()#获取刚刚上传图片数据的id
    image_id=upoload.id#获取当前上传用户的id

    sql='select id from wx_user'#查询所有用户的id
    try:
        cursor.execute(sql)
    except:
        database.ping(reconnect=True)
        cursor.execute(sql)
    
    
    user_id=cursor.fetchall()#获取所有用户的id

    #使用for/in循环对所有用户添加未读数据
    for (i,) in user_id:
        if(i==wxuser_id):
            continue

        info_data=information(user_id=i,image_id=image_id,equip_id=equip_id)#设备equip_id目前手动设置
        db.session.add(info_data)
        db.session.commit() 

        #将对应的设备未读信息数加一
        sql='update wx_user set info_number=info_number+1 where id=%s' %i
        cursor.execute(sql)
        database.commit()

    return ''


# 获取图片数据(缓存，修改过)
@imageapp.route('/getimagedata', methods=['GET', 'POST'],strict_slashes=True)
def getimagedata():
    imgsData = srch_hash_data('upload_img','init','')
    return imgsData
    # sql='select * from v_userImgs'
    # cursor.execute(sql)
    # imgs_data = cursor.fetchall()
    # json_data = json.dumps(imgs_data, cls=CJsonEncoder)
    # return json_data




# 按时间查找数据(缓存，修改过)
@imageapp.route('/search_time',strict_slashes=True)  # 查询数据使用GET请求
def srch_time():
    time = request.args.get('time')
    types = request.args.get('types')
    json_data = srch_hash_data(types,'date',time)
    return json_data


# 按名字查找数据(缓存，修改过)
@imageapp.route('/searchdata', methods=['GET', 'POST'],strict_slashes=True)
def imgdata():
    searchname = request.args.get('name')
    types = request.args.get('types')
    json_data = srch_hash_data(types,'name',searchname)
    return json_data

# 按id查找图片
@imageapp.route('/search_image', methods=['GET', 'POST'],strict_slashes=True)  # 查询数据使用GET请求
def search_image():
    imgsid = request.args.get('id')
    # imgsData = srch_hash_data('imgs','id',imgsid)
    # return imgsData
    sql = 'select image_desc,image_title,file_path,data_path from v_upImgs where upload_id=%s;' % imgsid
    cursor.execute(sql)
    results = cursor.fetchall()
    data = json.dumps(results, cls=CJsonEncoder)
    return data

# 按id下载数据
@imageapp.route('/export_data/<content>/<txtid>', methods=['GET', 'POST'],strict_slashes=True)  # 查询数据使用GET请求
def export_data(content,txtid):
    # imgsData = srch_hash_data('imgs','id',imgsid)
    # return imgsData
    sql = 'select data_path from v_upImgs where upload_id=%s;' %txtid
    cursor.execute(sql)
    results = cursor.fetchall()
    fullfilename = results[0][0]
    # fullfilename = '/root/allfile/123.txt'
    fullfilenamelist = fullfilename.split('/')
    filename = fullfilenamelist[-1]
    filepath = fullfilename.replace('/%s'%filename, '')
    #普通下载
    response = make_response(send_from_directory(filepath, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filepath.encode().decode('latin-1'))
    return send_from_directory(filepath, filename, as_attachment=True)


# 删除用户或图片的数据(缓存，修改过)
@imageapp.route('/delete', methods=['POST', 'GET'],strict_slashes=True)
def delete():
    types = request.form.getlist('types')
    types = ''.join(types)
    q = request.form.getlist('id')

    json_data = srch_hash_data(types,'delete',q)
    return json_data

# 新——数据导出获取图片数据(缓存，修改过)
@imageapp.route('/get_imagedata', methods=['GET', 'POST'],strict_slashes=True)
def get_imagedata():
    if len(r.keys('upload_img*')) == 0:
        sql='select distinct * from v_userImgs'
        cursor.execute(sql)
        user_data=cursor.fetchall()
        fields = cursor.description
        column_list = []
        json_list = []
        for i in fields:
            column_list.append(i[0])
        for row in user_data:
            data = {}
            for i in range(len(column_list)):
                data[column_list[i]] = row[i]
            json_list.append(data)
            imgsData = json.dumps(json_list,ensure_ascii=False,cls=CJsonEncoder)
        for i in range(len(user_data)):
            imgs_infor = {'name':user_data[i][0],'id':user_data[i][1],'user_id':user_data[i][2],'number':user_data[i][3],
                'date':user_data[i][4].strftime("%Y-%m-%d %H:%M:%S"),'equip_id':user_data[i][5],'image_desc':user_data[i][7],'image_title':user_data[i][6]}
            r.hmset('upload_img:%d'%(user_data[i][1]),imgs_infor)
            r.expire('upload_img:%d'%(user_data[i][1]),432000)
        return imgsData
    else:
        imgsdata = []
        for k in r.scan_iter('upload_img*'):
            data = r.hgetall(k)
            imgsdata.append(data)
        imgsdata = tuple(imgsdata)
        imgsdata = json.dumps(imgsdata,ensure_ascii=False,cls=CJsonEncoder)
        return imgsdata



############以下是ZIHUA - 资料分享站的资料管理页面后台代码##############
# 获取指定详情商品轮播图数据
@imageapp.route('/reviewVideo/<reviewId>', methods=['GET', 'POST'],strict_slashes=True)  
def reviewVideo(reviewId):
    reviewType,reviewId = reviewId.split('=')
    sql = 'select image_desc,image_title,data_path from v_upImgs where upload_id=%s;' % reviewId
    cursor.execute(sql)
    data = cursor.fetchall()
    picsData=[]
    for i in range(len(data)):
        picsInfor = {'image_desc':data[i][0],'image_title':data[i][1],'data_path':data[i][2]}
        picsData.append(picsInfor)
    json_data = json.dumps(picsData)
    return json_data


# 网页端图片上传，保存图片至本地(修改过)
@imageapp.route('/image_upload', methods=['POST', 'GET'],strict_slashes=True)
def web_imgsupload():
    user_phone = request.form.get('userPhone')
    user_name = request.form.get('userName')
    # t = request.form.get('uploadTime')
    t = '2021'
    desc = request.form.get('imageDesc')
    theme = request.form.get('imageTitle')
    number =request.form.get('imageCount')
    image = request.files.getlist('photo')

    basepath=os.path.split(os.path.dirname(__file__))[0]
    user = wx_user.query.filter(wx_user.phone == user_phone).first()  #获取用户名
    user_id = user.id  #获取用户ID
    upload_data = upload_img(user_id=user_id,number=number,equip_id=0,
        image_desc=desc,image_title=theme)  #将当前登录用户的id作为upload_img的user_id
    
    db.session.add(upload_data)
    db.session.commit()
    dire = "images/"
    file_path = Path(os.path.join(basepath, "static/"+ dire + user_name))  # 根据用户名创建文件夹
    base_path = Path(os.path.join(basepath,"static/"+ dire + user_name + "/" + t))   # 根据每次上传文件的时间戳创建文件夹
    
    for i in range(len(image)):
        filename = image[i].filename  #获取图片名
        if file_path.exists():  # 判断以用户名命名的文件夹是否存在
            if base_path.exists():  # 当以用户名命名的文件夹存在，则判断以当前获取的时间戳命名的文件夹是否存在
                if os.path.exists(filename):  # 判断发送的文件是否已经存在
                    # self.send(f"文件{filename}已经存在！")   
                    break                                            
                else:
                    file_name = "static/"+ dire + user_name+ "/" + t + "/" + filename
                    filename = os.path.join(basepath, "static/"+ dire + user_name + "/" + t + "/" + filename)  #路径拼接
                # 设置图片的真实存储路径
            else:  # 如果以用户名命名的文件存在，但不存在以当前获取的时间戳命名的文件夹,
                #则为创建文件夹，并为其创建一个获取的时间戳的文件夹，用于存放其发送到服务器的图片 
                os.mkdir(base_path)
                file_name = "static/"+ dire + user_name + "/" + t + "/" + filename
                filename = os.path.join(basepath, "static/"+ dire + user_name + "/" + t + "/" + filename)  #路径拼接
        else:  # 如果以用户名命名的文件夹不存在，则说明压根没登录过则为其创建一个以用户命名的文件夹，
            # 并将获取其传输过来的时间戳为其创建一个文件用于存放本次上传的图片                   
            os.mkdir(file_path)
            os.mkdir(base_path)
            file_name = "static/"+ dire + user_name + "/" + t + "/" + filename                  
            filename = os.path.join(basepath, "static/"+ dire + user_name + "/" + t + "/" + filename)  #路径拼接

        image[i].save(filename)
        print(filename)
        #将upload_img的id作为imgs的upload_id
        uploadid = upload_img.query.filter(
            upload_img.user_id == user_id).order_by(upload_img.date.desc()).first()
        up_id = uploadid.id  #获取当前上传用户的id,改id作为imgs.upload_id的外键
        img = imgs(upload_id=up_id, file_path=file_name, data_path=0)
        db.session.add(img)
        db.session.commit()
    return ''




