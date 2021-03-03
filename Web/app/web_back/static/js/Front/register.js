//注册
function register()
{
    var $userName = $("input[name='name']").val();
    var $pwd= $("input[name='passwd']").val();
    var $repwd= $("input[name='repasswd']").val();
    var $mailCode = $("input[name='email_code']").val();
    var $userPhone = $("input[name='phone']").val();
    var $userMail = $("#email").val()+$("#email_postfix").val();
    $('#register-confirm').addClass("disabled")
    $('#register-confirm').attr("disabled","disabled")
    if( !$userName || !$pwd || !$repwd  || !$userMail || !$mailCode || !$userPhone)
    {
        $('#register-confirm').removeClass("disabled")
        $('#register-confirm').removeAttr("disabled")
        layer.msg('必填项不能为空！', {
            time: 2000, //2000ms后自动关闭
        });
        return false
    }
    else
    {
        $.ajax({
            type: "POST",
            url: "/user/register/user_name="+$userName+"",
            data: { 
                username: $userName,
                pwd:$pwd,
                repwd:$repwd,
                usermail:$userMail,
                userphone:$userPhone,
                mailcode:$mailCode
            },
            success:function(data)
            {
                if(data==0)
                {
                    layer.msg('注册失败，验证码错误！<br>2s后自动跳转注册页面...', {
                    time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/user/admin_register';
                    }, 2000);                
                }
                 else if(data==1)
                {
                    layer.msg('注册成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    setTimeout(function (){
                        location.href='/user/admin_login';
                    }, 2000);
                    
                }
                else if(data==2)
                {
                    layer.msg('该用户名已经存在！', {
                    time: 2000, //2000ms后自动关闭
                    });                   
                }
                else
                {
                    layer.msg('注册失败，输入的信息不完整！<br>2s后自动跳转注册页面...', {
                    time: 2000, //3000ms后自动关闭
                    });               
                    setTimeout(function (){
                        location.href='/user/admin_register';
                    }, 2000);
                    
                }    
            }
        }); 
    }     
}

// $("html").keydown(function (event) {
//     if (event.keyCode == 13) 
//     {
//         console.log("执行回车");
//         register()
//     }
// });
$(document).keyup(function(event){ 
    if(event.keyCode ==13){ 
        console.log("执行回车");
        $("#register-confirm").trigger("click"); 
    } 
});

