//修改邮箱
function changeMail(){
    var $newMail= $("input[name='newmail']").val();
    var $oldMail = $("input[name='oldmail']").val();
    var $mail= $("input[name='email']").val();
    var $mailCode= $("input[name='mailcode']").val();
    if($oldMail==""||$newMail==""||$mail==""||$mailCode==""){
        pass;
    }

    else{
        var userID=$.cookie("userid");
        $.ajax({
            type: "POST",
            url: "/user/change_emails",
            data: { oldMail:$oldMail,newMail:$newMail,mailcode:$mailCode,userMail:$mail,userID:userID},
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


