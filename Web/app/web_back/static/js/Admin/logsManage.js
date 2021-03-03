var logsData;//储存全部json数据
var currentNum;//记录这是第几页
var pageNumber;	//总页数


$(document).ready(function () {

  //按时间查找信息
  layui.use('laydate', function searchTime(){
    var laydate = layui.laydate;
    //执行一个laydate实例
    laydate.render({
    elem: '#date' ,//指定元素
    done: function(date){    //根据时间查找信息
        web="search_time"//时间查找网址
        types="logs";
        var time = date;
        $.ajax({
          type: "GET",
          url: "/search_time",
          dataType: "json",
          data: { time: time,types:types },
          success: function (res) {
            $("#mode").empty();
            $(".page div").remove();
            $("#ID").val('');
            logsData = res;
            showData();
          }
        });
      // console.log(date);
      }
    });
    
  });

    

  //重置
  $("#reset").click(function reset(){
    web="getlogsdata";
    $("#date").val("");
    $("#ID").val('');
    $.ajax({
      url: "/getlogsdata",
      type: "get",
      dataType: "json",
      success: function (res) {
        $(".page div").remove();
        logsData = res;
        showData();
      }
    });
  })
// //关闭弹出层和遮罩层
//   $(".banner_img").click(function () {
//     $(".frame").fadeOut();
//     $(".fill").fadeOut();
//   })
 // 搜索名字
  $("#search").click(function searchName() {
    types="logs";
    var $name = $("#ID").val();
    console.log($name);
    $.ajax({
      type: "GET",
      url: "/searchdata",
      dataType: "json",
      data: { name: $name,types:types },
      success: function (res) {
        $('#date').val('');
        logsData = res;
        showData();
      },
      error: function () {
        console.log("获取数据失败");
      }
    });
  });


  // 删除日志
  $("#delAll").click(function delAll() {
    statistical();
    types="logs";
    var $ischk = $(":checkBox:checked");//获取选中框
    // console.log($ischk)
    $.ajax({
      type: "POST",
      url: "/delete",
      dataType: "json",
      data: {'id':IDArr,types:types},
      traditional:true,
      success: function (res) {
        alert("删除成功"); 
        // logsData=res;
        // showData();
        $ischk.each(function () {
          $(this).parent().parent().remove();
        })
      },
      error: function (res) {
        alert("删除失败");
      }
    });
  });

  
});



//查看日志
function reviewLogs(num){
    var ID=num;
    $.ajax({
      type: "GET",
      url: "/search_logs",
      dataType: "json",
      data: { id: ID },
      success: function (logs) {
        console.log(logs.length);
        console.log(logs);
            layui.use('layer', function(){
                var layer = layui.layer; 
                // for (var i = 0; i < logs.length; i++) 
                // { 
                    layer.open({
                    title: '日志信息'
                    ,content: '<table class="layui-table">\
                    <thead>\
                        <tr>\
                            <th>日志类型</th>\
                            <th>修改前信息</th>\
                            <th>修改后信息</th>\
                        </tr>\
                    </thead>\
                    <tbody id="mode2">\
                        <tr>\
                            <td>' + logs[0][0] + '</td>\
                            <td>' + logs[0][1] + '</td>\
                            <td>' + logs[0][2] + '</td>\
                        </tr>\
                    </tbody>\
                    </table>' 
                    });
                // }        
            });
      },
      error: function (logs) {
        alert("日志信息请求失败");
      }
    });
 
}


//初始化获取日志数据
$(function getData(){
	$("#reset").click();
});


//展示数据
function showData() 
{
    $("#checkall").prop("checked",false); 
    $("#mode").empty();
    $('.page').empty(); 
    var content;
    pageNumber = Math.ceil(logsData.length / 4);
    for (let j = 0; j < pageNumber; j++) //2ye
    {
        // var div = '<div id="PageNavId' + j + '"></div>';
        // $("#mode").append(div);
            for (let i = 0; i < 4; i++) 
            {
              // console.log((i + j * 4))
              // console.log(logsData.length)
                if ((i + j * 4) < logsData.length)   //onchange=chkChange('+i+')name="jcheck'+i+'"  bu id="see'+i+'" onclick="reviewLogs('+i+')"
                {
                  content ='<tr id="PageNavId' + j + '">\
                          <td><input id="jcheck" type="checkbox" onclick="clickOne()" name="jcheck" value="'+logsData[i + j * 4][0]+'">\
                          </td>\
                          <td>' + logsData[i + j * 4][0] + '</td>\
                          <td>' + logsData[i + j * 4][1] + '</td>\
                          <td>' + logsData[i + j * 4][2] + '</td>\
                          <td>' + logsData[i + j * 4][3] + '</td>\
                          <td>' + logsData[i + j * 4][8] + '</td>\
                          <td><button type="button" id="see'+logsData[i + j * 4][0]+'" onclick="reviewLogs('+logsData[i + j * 4][0]+')"  class="layui-btn layui-btn-normal">查看</button>\
                          </td>\
                        </tr>';
                  // $("#PageNavId" + j).append(content);
                  $("#mode").append(content);
                } 
                               
            } 
            if (j != 0) 
            {          
              var flag1 = "PageNavId" + (j).toString();
              var $trs = $("tr[id="+flag1+"]");
              for(let i=0;i<$trs.length;i++)
              {
                  $trs[i].style.display = "none";
              }
                // var flag = "#PageNavId" + (j).toString();
                // $(flag).hide();
            }
    }
          if ((pageNumber+1) <= 5) {//————————————————————————————————————————————————————
              for (let i = 1; i < (pageNumber+1); i++) {
                  if (i == 1 && (pageNumber+1) != 2) {
                      var content = '<span id="prev" href="javascript:void(0);" onclick="pageUper()">&laquo;</span>\
                      <span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>';
                      $('.page').append(content);
                  }
                  else if (i == (pageNumber+1)-1 && (pageNumber+1) != 2) {
                      var content = '<span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>\
                      <span id="next" href="javascript:void(0);" onclick="pageDowner()">&raquo;</span>';
                      $('.page').append(content);
                  }
                  else {
                      $('.page').append('<span id="num'+i+'" href="javascript:void(0);" onclick="separatePage(' + i + ')">' + i + '</span>');
                  }
              }
          }
          if ((pageNumber+1) > 5) {     //div=col-lg-1 pagenum变成了pagenum-1
              var jump = '<div class="layui-inline" style="width:20%;">\
              <input style="height:36px" type="text" id="page_input" placeholder="' + ((pageNumber+1) - 1) + '" autocompvare="off" class="layui-input">\
              </div>\
              <button style="height:36px" class="layui-btn layui-btn-sm" onclick="jumpPage()" id="go_btn" type="button">Go!</button>';
              var up=  '<span id="prev" href="javascript:void(0);" onclick="pageUper()">&laquo;</span>';

              var down= ' <span id="next" href="javascript:void(0);" onclick="pageDowner()">&raquo;</span> ';
                     
              $('.page').append(up);
              $('.page').append('<span id="num1" href="javascript:void(0);" onclick="separatePage(1)">1</span>');
              $('.page').append('<span id="num2" href="javascript:void(0);" onclick="separatePage(2)">2</span>');
              $('.page').append('<span id="num" href="javascript:void(0);">...</span>');
              $('.page').append('<span id="num'+ ((pageNumber+1) - 1) +'" href="javascript:void(0);" onclick="separatePage(' + ((pageNumber+1) - 1) + ')">' + ((pageNumber+1) - 1) + '</span>');
              $('.page').append(down);
              $('.page').append(jump);
          }
      
          separatePage(1);//————————————————————————————————————————————————————————————————————————————————————
        
}
      

