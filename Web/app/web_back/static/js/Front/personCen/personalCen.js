var userData;
var userID=$.cookie("userid");
function changePage(data)
{
    if (data=="1"){
    location.href='/user/change_password';
    }
    else if(data=="2"){
    location.href='/user/change_email';
    }
    else{
    location.href='/user/change_phone';
    }

}



$(document).ready(function personData() {

    $.getJSON("/user/getuserval",{userID:userID}, function (data) {
        $('#mode').empty();
        userData = data;
        showData();//展示数据
        }); 

});


function showData(){
    $('#mode').empty();
    console.log(userData);  
    var content ='<div class="layui-form-item">\
        <label class="layui-form-label" style="font-size:30px;color: rgb(0, 145, 125);">名称:</label>\
        <div class="layui-input-block">\
        <input name="username" lay-verify="required" style="font-size:15px;" placeholder="名称" value="' + userData[0][1] + '"  type="text" class="layui-input" disabled>\
        </div></div>\
        <hr class="hr12">\
        <div class="layui-form-item">\
        <label class="layui-form-label" style="font-size:30px;color: rgb(0, 145, 125);">手机:</label>\
        <div class="layui-input-block">\
        <input name="phone" lay-verify="required" style="font-size:15px;" placeholder="手机"   type="text" class="layui-input"value="' + userData[0][2] + '" disabled>\
        </div></div>\
        <hr class="hr12">\
        <div class="layui-form-item " style="font-size:30px;color: rgb(0, 145, 125);">\
        <label class="layui-form-label" ">邮箱:</label>\
        <div class="layui-input-block">\
        <input name="email" lay-verify="required" style="font-size:15px;" placeholder="邮箱"   type="text" class="layui-input" value="' + userData[0][3] + '" disabled>\
        </div></div>\
        <hr class="hr12">\
        <input value="修改密码" class="layui-input-inline"  type="button" onclick="changePage(1)">\
        <hr class="hr20" >\
        <input value="修改邮箱" class="layui-input-inline"   type="button" onclick="changePage(2)">\
        <hr class="hr20" >\
        <input value="修改手机号" class="layui-input-inline"  type="button" onclick="changePage(3)">\
        <hr class="hr20" >\
        <a href="/login_index/" style="color: rgb(0, 145, 125);margin-left: 270px;">返回首页</a>';
        $("#mode").append(content);
 
}
