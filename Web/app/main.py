from flask import Flask,make_response,session,request,render_template
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sockets import Sockets
from flask_mail import Mail
from web_back.common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor
from datetime import timedelta
from web_back.common import config
from web_back.model import models
from web_back.common.exts import db
# from views.user import getOpenid
from io import BytesIO

from web_back.controller import dataProcess
import gvcode
from web_back import create_app

app = create_app()
sockets = Sockets(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'  # 对话保护等级
login_manager.login_view = 'login'  # 定义登录的 视图
login_manager.login_message = '请登录以访问此页面'  # 设置快闪消息，定义需要登录访问页面的提示消息
login_manager.remember_cookie_duration = timedelta(days=7)  # 设置 cookie 的有效期，默认1年

db.init_app(app)

# 创建邮箱类实例
mail = Mail(app)


# 发送邮件函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# user_loader 回调函数,作用就是通过 id 返回对应的 User 对象。
@login_manager.user_loader
def load_user(id):
    return webuser.query.filter(webuser.id == id).first()

# 微信绑定邮箱发送验证码（需增加）
@app.route('/wx_bindemail', methods=['POST'],strict_slashes=True)
def wx_bindemail():
    code = "%06d" % random.randint(0, 999999)
    openid = request.values.get('openid')
    print(openid)
    user=wx_user.query.filter(wx_user.wx_id == openid).first()
    username=user.name
    usermail=request.values.get('bindmail')  
    codeKey = ""+ usermail +":code"
    r.setex(codeKey,120,code)#把code存进redis中,设置其60s过期时间
    try:
        msg = Message('ZIHUA - 资料分享站-验证邮件',
                      sender='351053928@qq.com',
                      recipients=[usermail])
        msg.body = 'sended by flask-email'
        msg.html = '<h1>Hi，Friend</h1></br>以下6位数字是邮箱验证码，请在小程序上填写以通过验证,验证码将在2分钟后过期。\
        </br>您的验证码为<h2 style=" width: 66px;background: #6777ef; border-radius: 4px; padding: 6px 12px;font-family: Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; \
        font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;">%s</h2>' % code
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
    except expression as identifier:
        print('发送失败')
    return ''

# 微信修改邮箱（新）
@app.route('/wx_update_mail', methods=['POST'],strict_slashes=True)
def wx_update_mail():
    openid=request.values.get('openid')
    newmail = request.form.get('newmail')
    mailcode = request.form.get('mailcode') 
    codeKey = ""+ newmail +":code"
    code = r.get(codeKey)
    if mailcode =='%s' % code:
        sql = 'update wx_user set email="'+newmail+'" where wx_id="'+openid+'"'
        cursor.execute(sql)
        database.commit()
        return jsonify({'status':'success'}) 
    else:
        return jsonify({'status':'fail'}) 

# 注册和修改信息发送邮件验证码
@app.route('/sendcode', methods=['POST'],strict_slashes=True)
def sendcode():
    code = "%06d" % random.randint(0, 999999)
    usermail = request.form.get('userMail')
    codeKey = ""+ usermail +":code"
    r.setex(codeKey,120,code)#把code存进redis中,设置其60s过期时间
    try:
        msg = Message('ZIHUA - 资料分享站-验证邮件',
                      sender='351053928@qq.com',
                      recipients=[usermail])
        msg.body = 'sended by flask-email'
        msg.html = '<h1>Hi，Friend</h1></br>以下6位数字是邮箱验证码，请在网站上填写以通过验证,验证码将在2分钟后过期。\
        </br>您的验证码为<h2 style=" width: 66px;background: #6777ef; border-radius: 4px; padding: 6px 12px;font-family: Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; \
        font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;">%s</h2>' % code
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
    except expression as identifier:
        print('发送失败')
    return ''

#网页用户找回帐号密码(修改过)
@app.route('/findloss', methods=['GET'], strict_slashes=True)
def findloss():
    usermail = request.form.get('userMail')
    sql = 'select *from wx_user where email="' + usermail + '"'
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) == 0:
        print('发送失败')
        return ("0")
    else:
        msg = Message('帐号密码找回',
                      sender='351053928@qq.com',
                      recipients=[usermail])
        msg.body = 'sended by flask-email'
        msg.html = '<b>您的帐号为%s，密码为%s<b>' %(data[0][1],data[0][4])
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()
    
        return ("1")  

@sockets.route('/')
def tran_data(ws):
    rec = ReciveData(ws)
    rec.runThread()



@app.route('/', strict_slashes=True)
def index():
    return render_template('index.html')
    

# 获取登录的验证码
@app.route('/get_imageCode',methods=['GET'],strict_slashes=True)
def get_imageCode():
    # 生成验证码图片
    image, code = gvcode.generate()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['imageCode'] = code
    verify_code = session.get('imageCode')
    print(verify_code)
    return response

if __name__=='__main__':

    app.run(debug=True) 
 


