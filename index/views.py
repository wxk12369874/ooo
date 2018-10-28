import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def index_views(request):
    return render(request,'index.html')

# /login 对应的视图
def login_views(request):
    url = '/'
    if request.method == 'GET':
        # get 的流程
        # 判断session中是否有登录信息
        if 'uid' in request.session and 'uphone' in request.session:
            # session中有值,重定向回首页或原路径
            print('session中有数据')
            return redirect(url)
        else:
            # session中没有值
            # 判断cookie中是否有uid和uphone
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                # cookie 中有登录信息
                # 从cookie中取出数据保存进session
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid']=uid
                request.session['uphone']=uphone
                # 重定向到首页或原路径
                return redirect(url)
            else:
                # cookie 中没有登录信息
                # 去往登录页面
                form = LoginForm()
                return render(request,'login.html',locals())
    else:
        # post 的流程
        # 实现登录操作：取出uphone和upwd到db中判断
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uList = Users.objects.filter(uphone=uphone,upwd=upwd)
        if uList:
            # 登录成功
            uid = uList[0].id
            # 取出 uphone 和 uid 保存进session
            request.session['uid'] = uid
            request.session['uphone'] = uphone
            # 判断是否有记住密码，记住密码的话则将值保存进cookie
            resp = redirect(url)
            if 'isSaved' in request.POST:
                # 记住密码，保存进cookie
                expires = 60 * 60 * 24 * 366
                resp.set_cookie('uid',uid,expires)
                resp.set_cookie('uphone',uphone,expires)
            # 重定向到首页或原路径
            return resp
        else:
            #登录失败 ： 回登录页
            form = LoginForm()
            errMsg = "用户名或密码不正确"
            return render(request,'login.html',locals())

# /register 对应的视图
def register_views(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        #实现注册的功能
        dic ={
            "uphone":request.POST['uphone'],
            "upwd":request.POST['upwd'],
            "uname":request.POST['uname'],
            "uemail":request.POST['uemail'],
        }
        #将数据插入进数据库 - 注册
        Users(**dic).save()
        #根据uphone的值再查询数据库
        u = Users.objects.get(uphone=request.POST['uphone'])
        #将用户id和uphone保存进session
        request.session['uid'] = u.id
        request.session['uphone'] = u.uphone

        return redirect('/')

# 检查手机号码是否存在 -> /check_uphone/
def check_uphone_views(request):
    if request.method == 'POST':
        #接收前端传递过来的手机号码
        uphone = request.POST['uphone']
        uList = Users.objects.filter(uphone=uphone)
        if uList:
            # 如果条件为真，则表示手机号码已经存在
            # 响应 status值为0，用于通知客户端手机号码已存在
            # 响应 text值为 “手机号码已存在”
            dic = {
                "status":"0",
                "text":'手机号码已存在',
            }
            return HttpResponse(json.dumps(dic))
        else:
            dic = {
                "status":"1",
                "text":"可以注册",
            }
            return HttpResponse(json.dumps(dic))

# 检查用户是否登录，如果有的话则取出uname的值
def check_login_views(request):
    # 判断 session 中是否有 uid 和 uphone
    if 'uid' in request.session and 'uphone' in request.session:
        # 用户此时处于登录状态
        # 根据 uid 获取 uname 的值
        uid = request.session['uid']
        user = Users.objects.get(id=uid)
        #处理响应数据
        dic = {
            "status":'1',
            'user':json.dumps(user.to_dict())
        }
        return HttpResponse(json.dumps(dic))
    else:
        # 判断cookie是否有登录信息
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            # 从cookie中取出数据保存进session
            uid = request.COOKIES['uid']
            uphone = request.COOKIES['uphone']
            request.session['uid']=uid
            request.session['uphone']=uphone
            # 根据uid查询处对应的user信息转换成字典，响应给客户端
            user = Users.objects.get(id=uid)
            jsonStr = json.dumps(user.to_dict())

            dic = {
                "status":"1",
                "user":jsonStr,
            }
            return HttpResponse(json.dumps(dic))
        else:
            # session和cookie中都没有登录信息
            dic = {
                "status":0,
                'text':'用户尚未登录'
            }
            return HttpResponse(json.dumps(dic))

# 退出登录
# 清除 session 和 cookie 中的数据
# 原路返回
def logout_views(request):
    #获取请求源地址，如果没有，则返回首页 /
    url = request.META.get('HTTP_REFERER','/')
    resp = redirect(url)
    # 判断 session 中是否有登录信息
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        resp.delete_cookie('uid')
        resp.delete_cookie('uphone')

    return resp

# 查询出所有的商品类型以及每个类型下的前10个商品
def type_goods_views(request):
    all_list = []
    # 查询所有的商品类型
    types = GoodsType.objects.all()
    for type in types:
        # 将得到的type对象转换成JSON字符串
        type_json = json.dumps(type.to_dict())
        # 获取type下所有的商品（取前10个）
        g_list=type.goods_set.order_by("-price")[0:10]
        # 将前10个商品转换成JSON串
        g_list_json=serializers.serialize('json',g_list)
        # 将type_json 以及 g_list_json 封装到一个字典中，再追加到 all_list列表中
        dic = {
            'type':type_json,
            'goods':g_list_json,
        }

        all_list.append(dic)

    return HttpResponse(json.dumps(all_list))

#添加或更新数量到购物车
def add_cart_views(request):
    #接收数据
    users_id = request.session['uid']
    goods_id = request.GET['goods_id']
    # 接收购买数量，如果没有的话，则默认为１
    ccount = request.GET.get('ccount',1)

    #查看购物车中是否有相同用户购买过相同商品，如果有的话则更新数量，没有的话则新增数据
    cart_list = CartInfo.objects.filter(users_id=users_id,goods_id=goods_id)
    if cart_list:
        #已经有商品，更新购买数量
        cartinfo = cart_list[0]
        cartinfo.ccount = cartinfo.ccount + int(ccount)
        cartinfo.save()
        dic = {
            'status':'1',
            'text':'更新数量成功',
        }
        return HttpResponse(json.dumps(dic))
    else:
        #创建商品并保存进数据库
        cartinfo = CartInfo()
        cartinfo.users_id = users_id
        cartinfo.goods_id = goods_id
        cartinfo.ccount = int(ccount)
        cartinfo.save()
        dic = {
            'status':'1',
            'text':'添加至购物车成功',
        }
        return HttpResponse(json.dumps(dic))


# 查询某用户购物车内的商品数量
def cart_count_views(request):
    if 'uid' not in request.session:
        dic = {
            'count':0
        }
        return HttpResponse(json.dumps(dic))
    else:
        uid = request.session['uid']
        all_cart = CartInfo.objects.filter(users_id=uid)
        total_count = 0
        for cart in all_cart:
            total_count += cart.ccount
        dic = {
            "count":total_count
        }
        return HttpResponse(json.dumps(dic))




