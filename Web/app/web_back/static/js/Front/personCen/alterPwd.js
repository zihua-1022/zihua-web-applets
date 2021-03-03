//修改密码
function changePwd(){
    // var $userMail = $("input[name='email']").val();
    var $oldPwd= $("input[name='oldpwd']").val();
    var $newPwd= $("input[name='newpwd']").val();
    var $mailCode= $("input[name='mailcode']").val();
    var $mail= $("input[name='email']").val();
    if($oldPwd=="" || $newPwd==""||$mail==""||$mailCode==""){
        pass;
    }

    else{
        var userID=$.cookie("userid");
        $.ajax({
            type: "POST",
            url: "/user/change_passwords",
            data: { oldpwd:$oldPwd,newpwd:$newPwd,mailcode:$mailCode,userMail:$mail,userID:userID},
            success:function(data){
                if(data==0){
                    layer.msg('修改成功！', {
                    time: 2000, //2000ms后自动关闭
                    });
                    location.href='/personal_cental';  
                }
                else{
                    layer.msg('验证码错误！', {
                    time: 2000, //2000ms后自动关闭
                    });  
                }
            }    
        });
    }
}