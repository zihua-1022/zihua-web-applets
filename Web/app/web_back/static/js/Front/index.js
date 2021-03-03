$(function checkLogIn(){
    var userid=$.cookie("userid");
    layui.use('layer', function(){
        var layer = layui.layer;
     
        if(userid!=null && userid!="")
        {
            $.ajax({
            type: "GET",
            url: "/user/check_users",
            data: { userid: userid},
            success:function(data)
            {
                if(data==2)
                {
                    layer.msg('已经登录！', {
                        time: 2000, //2000ms后自动关闭
                        });
                        setTimeout(function (){
                            location.href='/user/admin_manage';
                        }, 2000);
                }
            }
            });
        }
    });
});