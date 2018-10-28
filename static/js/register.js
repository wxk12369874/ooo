/**
 * Created by tarena on 18-9-5.
 */
/**
 * 功能：检查手机号码是否符合规范
 * 返回值：
 *  true:通过验证
 *  false:未通过验证
 * */
function checkUphone(){
    var value = $("[name='uphone']").val();
    //向window对象中增加一个变量flag，默认值为false
    window.flag = false;
    //去掉value两端的空格后，在验证长度
    if(value.trim().length == 11){

        //验证手机号码是否存在
        $.ajax({
            url:"/check_uphone/",
            type:'post',
            //data:'uphone='+value,
            data:{
                uphone:value,
                csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
            },
            async:false,
            dataType:'json',
            success:function(data){
                $("#uphone-show").html(data.text);
                if(data.status == 1) {
                    window.flag = true;
                }
                else {
                    window.flag = false;
                }
            }
        });
    }else{
        $("#uphone-show").html('手机号码位数不正确');
        window.flag = false;
    }
    return window.flag;
}

/**
 * 功能：检查密码是否符合规范
 * 规范：
 *  1.必须是6位以上
 * 返回值：
 *  true：通过验证
 *  false：未通过验证
 * */
function checkUpwd(){
    var upwd = $("[name='upwd']").val();
    if(upwd.length >= 6){
        $("#upwd-show").html("通过");
        return true;
    }
    $("#upwd-show").html("密码不符合规范");
    return false;
}

/**
 * DOM树加载完毕时要执行的操作
 * 包含初始化的行为操作 如：事件的绑定
 * */
$(function(){
    /**为 name=uphone 的元素绑定 blur 事件*/
    $("[name='uphone']").blur(function(){
        checkUphone();

    });

    /**为 name=upwd 的元素绑定 blur 事件*/
    $("[name='upwd']").blur(function(){
        checkUpwd();
    });

    /**为 #frmRegister 绑定 submit 事件*/
    $("#frmRegister").submit(function(){
        return checkUphone() && checkUpwd();
    });
});







