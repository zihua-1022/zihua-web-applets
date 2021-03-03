var twoFA = false;
$ (function (){
    $("input[name='remember']").prop("checked", true);   //将其value值设置为真true
});

//登录
function logIn()
{
    var $phone_email = $("input[name='phone_email']").val();
    var $password= $("input[name='password']").val();
    var $code = $("#2fa-code").val();
   

    if(!$phone_email || !$password)
    {
        layer.msg('必填项不能为空！', {
            time: 2000, //2000ms后自动关闭
        });
        return false;    
    }
    else if(twoFA == true) 
    {
        if (!$("#2fa-code").val())
        {
          return false;
        }
    }
    else
    {
        $.ajax({
            type: "POST",
            url: "/user/check_user",
            data: {
                userphone: $phone_email,
                password:$password,
                code:$code,
                remember_me: $("#remember-me:checked").val()        
            },
            dataType:"json",
            success: function(data)
            {
                if(data==0)
                {
                    layer.msg('验证码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $("#2fa-code").val('');
                    $("img[name='img_code']").click();
                    // $('.login-form-item').hide('500');
                    // $('form').removeClass('was-validated');
                    // $('#2fa-form').show('fast');
                }
                else if(data==1)
                {
                    layer.msg('帐号密码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $("input[name='password']").val('');
                    // $("input[name='code']").val('');
                    // $("img[name='img_code']").click();
                    // var errorMsg = '密码或邮箱不正确';
                    // if (twoFA == true) 
                    // {
                    //   errorMsg = '两步验证码错误'
                    // }
                    // swal('出错了', errorMsg, 'error');
                }
                else
                {
                    layer.msg('登录成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    $.cookie("userid",data[0],{expires:7,path:"/"});
                    localStorage.username = data[1];//储存用户名
                    localStorage.userphone = $phone_email
                    setTimeout(function (){
                        location.href='/user/admin_manage';
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
//         logIn();
//     }
// });

$(document).keyup(function(event){ 
    if(event.keyCode ==13){ 
        console.log("执行回车");
        $("#login-confirm").trigger("click"); 
    } 
});

