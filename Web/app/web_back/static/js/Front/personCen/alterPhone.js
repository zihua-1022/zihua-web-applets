//修改电话
function changePhone(){
    var $oldPhone= $("input[name='oldphone']").val();
    var $newPhone= $("input[name='newphone']").val();
    var $mailCode= $("input[name='mailcode']").val();
    var $mail= $("input[name='email']").val();
    if($oldPhone=="" || $newPhone==""||$mail==""||$mailCode==""){
    pass;
    }

    else{
        var userID=$.cookie("userid");
        $.ajax({
            type: "POST",
            url: "/user/change_phones",
            data: { oldPhone:$oldPhone,newPhone:$newPhone,mailcode:$mailCode,userMail:$mail,userID:userID},
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