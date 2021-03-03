var imageCount;  //总的图片数量
var existCount;  
var dataArr = []; // 储存所选图片的结果
var ID =0;   
var formFile = new FormData(); //FormData方式发送请求
userName=localStorage.username;
userPhone=localStorage.userphone 
var userID=$.cookie("userid");
var $imageTitle
var $imageDesc


if(typeof FileReader == 'undefined')
{
    alert('抱歉，你的浏览器不支持 FileReader');
    $('#file_input').setAttribute('disabled','disabled');
}
else
{
    $(function (){
        $('#file_input').change(readFile);

    })
    
}　

//预览图片及限制一次上传图片数量事件
function readFile()
{
   
    var allImage=this.files; //获取所有图片
    imageCount = allImage.length;
    if((imageCount+existCount) > 8)
    {
        
        alert('图片数不能超过8个，你选择了' + (imageCount*1+existCount*1) + '个,请重新选择');
        imageCount = 0;
        // return false;
        $(function(){
            $('#add').click();
        });
    }
    else 
    {
        for(let i=0;i<imageCount;i++)
        {
            //判断上传文件格式
            if (!($('#file_input').val()).match(/.jpg|.gif|.png|.jpeg|.bmp/i))
            {　　
                return alert('上传的图片格式不正确，请重新选择');
            }
            else
            {
            
                var getImage = allImage[i];  //获取图片
                dataArr[ID] = getImage;
                ID++;
                var url = URL.createObjectURL(getImage); //获取图片路径
                var showImage = document.createElement('img');
                showImage.setAttribute('src', url);
                showImage.className = 'showImage';
                var div = document.createElement('div'); //创建一个div

                div.className = 'float';
                var deleteBox = document.createElement('div');
                deleteBox.className = 'delete';
                deleteBox.innerText = 'delete';  
                deleteBox.id = allImage[i].name;
                div.appendChild(deleteBox);
                div.appendChild(showImage);
                // div2.appendChild(image_title);
                // '<div class='delete' id=''+allImage[i].name+''>delete</div>\
                // document.getElementsByTagName('body')[0].appendChild(div);  　　//插入dom树  即显示选择的图片
                $('.imgs_container').append(div);
               
            }

        }
        $('.image_title').css({display : 'block'}).fadeIn();
        $('.image_desc').css({display : 'block'}).fadeIn(); 

    }
    //删除图片事件
    $('.delete').click(function(){
        var $fileName = $(this).attr('id');
        $(this).parent().remove();  //删除父节点
        // console.log(dataArr)
        var fileList = Array.from(dataArr);  //遍历数组
        for (let j = 0; j < fileList.length; j++) 
        {
         
            //通过图片名判断图片在数组中的位置然后删除
            // console.log(fileList[j].name+'111');
            if (fileList[j].name == $fileName) 
            {
                
                fileList.splice(j, 1);   //删除位于 index j 的元素
                ID--;
                break;
            }

        }
        dataArr = fileList;
        console.log(dataArr)
    })
    
}
//显示图片
var $img = $('.float img');
$img.onload = function imgs()
{
    //设置图片大小
    var nowHeight = ReSizePic(this);
    this.parentNode.style.display = 'block';
    var oParent = this.parentNode;
    if(nowHeight)
    {
        oParent.style.paddingTop = (oParent.offsetHeight - nowHeight)/2 + 'px';
    }

}

//追加图片事件
$(function (){
    $('#add').click(function(){
        statistical();
        $('#file_input').val('');   // 先将$('#file_input')值清空，否则选择图片与上次相同时change事件不会触发
        $('#file_input').click();
        
    });
});
//上传图片事件
$(function (){
    $('#upload').click(function()
    {
        $imageTitle = $('#image_title').val();
        $imageDesc =  $('#image_desc').val();
        appendData();
        console.log(formFile);
        if(!imageCount)
        {
            return alert('请先选择文件');
        }
        else
        {
            if(userName!=null&&userName!='')
            {
                uploadImages();
            }           
            
        }
    });
});
//设置预览的图片
function ReSizePic(ThisPic) 
{
    var RePicWidth = 200; //这里修改为您想显示的宽度值
    var TrueWidth = ThisPic.width; //图片实际宽度
    var TrueHeight = ThisPic.height; //图片实际高度
    if(TrueWidth>TrueHeight)
    {
        //宽大于高
        var reWidth = RePicWidth;
        ThisPic.width = reWidth;
        //垂直居中
        var nowHeight = TrueHeight * (reWidth/TrueWidth);
        return nowHeight;  //将图片修改后的高度返回，供垂直居中用
    }
    else
    {
        //宽小于高
        var reHeight = RePicWidth;
        ThisPic.height = reHeight;
    }
}
//统计当前页面上的图片数量
function statistical()
{ 
    var array = []; //储存统计结果
    $('.delete').each(function(){
        array.push($(this).attr('id'));
    });
    imageCount=array.length;  //上传图片总数
    existCount=array.length;
}
//图片信息dataArr追加到formFile里
function appendData()
{
    statistical();
    for(let i=0;i<dataArr.length;i++)
    {
        // formFile.append('file',$('#file_input').get(0).files[aaa[i]]);  //得到file的第几行文件
        formFile.append('photo',dataArr[i]);
    } 
    console.log(imageCount,$imageDesc,$imageTitle,userPhone,userName)
    formFile.set('imageCount',imageCount); 
    formFile.set('imageTitle',$imageTitle);   
    formFile.set('imageDesc',$imageDesc);  
    formFile.set('userPhone',userPhone);  
    formFile.set('userName',userName);   

                  
}
//请求上传图片事件
function uploadImages()
{
    $.ajax({
        type: 'POST',
        url: '/image/image_upload',
        data : formFile,
        async:false,//同步请求 
        processData:false,
        contentType:false,
        /**
        用ajax发送formFile参数时要告诉jQuery不要去处理发送的数据，
        不要去设置Content-Type请求头才可以发送成功，否则会报“Illegal invocation”的错误，
        也就是非法调用，所以要加上“processData: false,contentType: false,”
        */
        success: function (data) {
            alert('图片上传成功');
            location.replace(location);
        },
        error: function (data) {
            alert('图片上传失败');
        }
    });
}
