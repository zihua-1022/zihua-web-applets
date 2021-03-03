var userid=$.cookie("userid");
username=localStorage.username;
$(function(){
    $('#current_user').append(username);
})


//退出登录
function exits()
{ 
    try
    {
                  
        $.cookie("userid","",{expires:7,path:'/'});
        $.ajax({
            type: "POST",
            url: "/user/clearkey",
            data: {userid:userid},
        });
        layer.msg('退出成功！', {
        time: 2000, //2000ms后自动关闭
        });
        setTimeout(function (){
            location.href='/';
        }, 2000); 
    }
    catch(err)
    {
        alert("错误");
        var script=document.createElement("script");
        script.type="text/javascript";
        script.src='https://cdn.bootcdn.net/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.js';
        document.getElementsByName("head")[0].appendChild(script);
        script.onload=function(){
        $.cookie("userid","",{expires:7,path:'/'});
        location.href='/user/user_manage';

        }
    }
}
