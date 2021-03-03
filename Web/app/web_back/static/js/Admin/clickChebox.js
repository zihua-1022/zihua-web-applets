// document.write("<script language=javascript src='/js/iamgemanage.js'></script>");
var clicks=1; //选择单页点击按钮状态
var IDArr=[]; //储存id信息


//选择单页事件
function clickOnePage()
{  
    console.log(currentNum)
    var flag = "#PageNavId" + (currentNum-1);
    if(clicks%2==1){
      $(""+flag+" input[type='checkbox']").prop("checked", true);   //将其value值设置为真true
      $('#checkonepages').text('取消单页');
    }
    if(clicks%2==0){
      console.log('选择');
      $(""+flag+" input[type='checkbox']").prop("checked", false);   //将其value值设置为假
      $('#checkonepages').text('选择单页');
    }
      clicks++;
      var $jcheck = $("input[id=jcheck]");
      $("#checkall").prop("checked", $jcheck.length == $jcheck.filter(":checked").length ? true : false);
}

//主要是用来统计选中的复选框的ID或选中第几行数据
function statistical()
{
    var array = [];
    $.each($("#mode").find("input:checked"), function () {
        array.push($(this).val());
        IDArr=array;
    });
}

//全选事件
function clickAll() 
{
      if ($("#checkall").prop("checked")) // 全选 
      { 
          $("input[name='jcheck']").each(function()   //取当前页面所有name='check_name'的input元素，循环每一个取到的元素,
          {
            $(this).prop("checked", true);   //将其value值设置为真true
          });
          $('#checkonepages').text('取消单页');
          clicks = 0;
      }
      else   // 取消全选 
      { 
          $("input[name='jcheck']").each(function () {
            $(this).prop("checked", false);
          });
          $('#checkonepages').text('选择单页');
          clicks = 1;
      }
}

//单选
function clickOne() 
{
    console.log(44444);
    var flag = "#PageNavId" + (currentNum-1);
    var flag1 = "PageNavId" + (currentNum-1).toString();
    var $trs = $("tr[id="+flag1+"]");
    var $clickCount=$(""+flag+" input[type='checkbox']:checked").length;
    var $jcheck = $("input[id=jcheck]");
    $("#checkall").prop("checked", $jcheck.length == $jcheck.filter(":checked").length ? true : false);
    if($clickCount != $trs.length)
    {
      $('#checkonepages').text('选择单页');
      clicks = 1;
    }
    else
    {
      $('#checkonepages').text('取消单页');
      clicks = 0;
    }
}


$(function(){

  //刷新渲染
  layui.use(['form', 'code'], function () {
    layui.form.render();   
  });  
    // $("#checkall").click( function () {
    //   console.log("qqqq");
    //     $("input[type=checkbox]").prop("checked", this.checked);
    //     $("input[type=checkbox]").prop("checked", this.checked);
    //     if($(this).prop("checked")==true)
    //     {
    //       $('#checkonepages').text('取消单页');
    //         clicks = 0;
    //     }
    //     else
    //     {
    //       $('#checkonepages').text('选择单页');
    //         clicks = 1;
    //     }
    // });


    // //全选与单选
    // $("input[name=jcheck]").click( function() {
    //     console.log("wwwww");
    //     var flag = "#PageNavId" + (currentNum-1);
    //     var flag1 = "PageNavId" + (currentNum-1).toString();
    //     var $trs = $("tr[id="+flag1+"]");
    //     var $clickCount=$(""+flag+" input[type='checkbox']:checked").length;
    //     var $jcheck = $("input[id=jcheck]");
    //     $("#checkall").prop("checked", $jcheck.length == $jcheck.filter(":checked").length ? true : false);
    //     if($clickCount != $trs.length)
    //     {
    //         $('#checkonepages').text('选择单页');
    //         clicks = 1;
    //     }
    //     else
    //     {
    //         $('#checkonepages').text('取消单页');
    //         clicks = 0;
    //     }
    // });
});
 

// //分页
// function separatePage(page) 
// {
//     currentNum = page;
//     switchPageNum(page,pageNumber)
//     for (let i = 0; i < pageNumber; i++) 
//     {
//         if (i + 1 == page)  //第一页
//         {
          
//           var flag = "#PageNavId" + (i).toString();
//           var flag1 = "PageNavId" + (i).toString();
//           var $trs = $("tr[id="+flag1+"]");
//           for(let i=0;i<$trs.length;i++)
//           {
//               $trs[i].style.display = "";
//           }

//         //     $(flag).show();
//         }
//         else 
//         {
            
//             var flag = "#PageNavId" + (i).toString();
//             var flag1 = "PageNavId" + (i).toString();
//             var $trs = $("tr[id="+flag1+"]");
//             for(let i=0;i<$trs.length;i++)
//             {
//                 $trs[i].style.display = "none";
//             }
//             // $(flag).hide();
//         }
//     }

//     var flag = "#PageNavId" + (currentNum-1);
// 	  var flag1 = "PageNavId" + (currentNum-1).toString();
//     var $trs = $("tr[id="+flag1+"]");
//     var $clickCount=$(""+flag+" input[type='checkbox']:checked").length;
//     if($clickCount == 0)
//     {
//       $('#checkonepages').text('选择单页');
//       clicks=1;
//     }
//     if($clickCount == $trs.length)
//     {
//         $('#checkonepages').text('取消单页');
//         clicks=0;
//     }
//     console.log(clicks);
// }

// //上一页————————————————————
// function pageUper() 
// {
//   if (currentNum > 1) {
//     separatePage(currentNum - 1);
//   }

// }
// //下一页——————————————————————————————————
// function pageDowner() 
// {
//   if (currentNum < pageNumber) {
//     separatePage(currentNum + 1);
//   } 
    
// }

// //多页，用来输入框跳转
// function jumpPage() 
// {
//     separatePage($('#page_input').val()*1);
// }


// function switchPageNum(page,pageNumber)
// {
//     $('.current').removeAttr("class",'current');
//     $('#num'+page+'').attr('class','current');
//     if(page > 2 && page < pageNumber)
//     {
//       $('#num').attr('class','current');
//     }
 
// }




