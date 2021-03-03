from flask import Blueprint,request,render_template,url_for,json
from web_back.model.models import logs,logs_type
from web_back.common import myForms
from flask_login import current_user,login_user
from web_back.common.searchData import CJsonEncoder,srch_hash_data,r,database,cursor


# 实例化一个蓝图
logsapp=Blueprint('logs',__name__,template_folder="../templates",static_folder="../static")


# 日志管理
@logsapp.route('/logs_manage',strict_slashes=True)
def logs_manage():
    return render_template('logs_manage.html')


# 获取管理员日志数据
@logsapp.route('/getlogsdata', methods=['GET', 'POST'],strict_slashes=True)
def getlogsdata():
    sql = 'select *from logs'
    cursor.execute(sql)
    logs_data = cursor.fetchall()
    json_data = json.dumps(logs_data, cls=CJsonEncoder)
    return json_data  


# 根据id查看日志信息
@logsapp.route('/search_logs',methods=['GET','POST'],strict_slashes=True)
def search_logs():
    userID=request.args.get('id')
    sql='select logs_type.logs_typename,logs.beinfo,logs.afinfo from logs_type left join logs on logs_type.id=logs.logs_typeid where logs.id=%s' %userID
    cursor.execute(sql)
    logs_data=cursor.fetchall()
    json_data=json.dumps(logs_data,cls=CJsonEncoder)
    return json_data


# 新——数据导出获取日志数据(导出数据要添加最上面的标题)
@logsapp.route('/get_logsdata', methods=['GET', 'POST'],strict_slashes=True)
def get_logsdata():
    sql = 'select *from logs'
    cursor.execute(sql)
    logs_data=cursor.fetchall()
    fields = cursor.description
    column_list = []
    json_list = []
    for i in fields:
        column_list.append(i[0])
    for row in logs_data:
        data = {}
        for i in range(len(column_list)):
            data[column_list[i]] = row[i]
        json_list.append(data)
    logsdata = json.dumps(json_list,ensure_ascii=False,cls=CJsonEncoder)
    return logsdata
