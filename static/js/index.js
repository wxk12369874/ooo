/**
 * Created by tarena on 18-9-6.
 */
/**
 * 功能：检查登录状态(AJAX)
 *  如果有登录信息的话，登录位置处显示 ： 欢迎 xxxx 退出
 *  如果没有登录信息的话，登录位置处显示：[登录][注册有惊喜]
 * */
function check_login(){
    $.get('/check_login/',function(data){
        var html = "";
        if(data.status == 0){
            html+="<a href='/login'>[登录]</a>,";
            html+="<a href='/register'>[注册有惊喜]</a>";
        }else if(data.status == 1){
            //用户已经处于登录状态
            user = JSON.parse(data.user)
            html+="欢迎:"+user.uname+"&nbsp;&nbsp;";
            html+="<a href='/logout/'>退出</a>";
        }
        $("#list>li:first").html(html);
    },'json');
}

/**
 * 功能：加载所有的商品分类以及对应的商品
 * */
function loadGoods(){
    $.get('/type_goods/',function(data){
        var html="";
        //循环遍历data,得到类别以及对应的商品JSON
        $.each(data,function(i,obj){
            html+="<div class='item'>";
            var typeObj = JSON.parse(obj.type);
              html+="<p class='title'>";
                html+="<a href='#'>更多</a>";
                html+="<img src='/"+typeObj.picture+"'>";
              html+="</p>";
              html+="<ul>";
                //将obj.goods转换成JSON数组
                var goodsArr = JSON.parse(obj.goods);
                $.each(goodsArr,function(i,goods){
                  //goods表示的是每一个商品
                  html+="<li ";
                  if((i+1) % 5 == 0)
                    html+="class='no-margin'";
                  html+=">";
                    //加载商品图片
                    html+="<p>";
                      html+="<img src='/"+goods.fields.picture+"'>";
                    html+="</p>";
                    //加载商品内容
                    html+="<div class='content'>";
                      //加载购物车标识
                      html+="<a href='javascript:add_cart("+goods.pk+");' class='cart'>";
                        html+="<img src='/static/images/cart.png'>";
                      html+="</a>";
                      //加载商品标题
                      html+="<p>"+goods.fields.title+"</p>";
                      //加载商品价格以及规格
                      html+="<span>&yen;"+goods.fields.price+"/"+goods.fields.spec+"</span>";
                    html+="</div>";
                  html+="</li>";
                });
              html+="</ul>";
            html+="</div>";
        });

        $("#main").html(html);
    },'json');
}

/**
 * 功能：将指定的商品添加至购物车
 * 参数：goods_id , 表示的是要加入到购物车的商品的id
 * */
function add_cart(goods_id){
  //检查用户是否处于登录状态
  $.get('/check_login/',function(data){
    if(data.status == 0){
      alert('请先登录... ...');
    }else{
      $.get(
        '/add_cart/',
        'goods_id='+goods_id,
        function(data){
          if(data.status == 1){
            alert("添加购物车成功!");
            //加载当前用户的购物车内商品的数量
            load_count();
          }else{
            alert('添加购物车失败!');
          }
        },
        'json');
    }
  },'json');
}

/** 功能：加载当前用户的购物车中的商品数量*/
function load_count(){
  $.get('/cart_count/',function(data){
    $("#myCart>a").html("我的购物车("+data.count+")");
  },'json');
}




/**
 * 功能：网页加载时要执行的操作
 * */
$(function(){
    //检车登录状态 - check_login()
    check_login();
    //加载所有商品类别以及商品信息
    loadGoods();
    //加载当前用户的购物车内商品的数量
    load_count();
});