from django.conf.urls import url
from .views import *
urlpatterns = [
    #访问路径是 /
    url(r'^$',index_views),
    #访问路径是 /login
    url(r'^login/$',login_views),
    #访问路径是 /register
    url(r'^register/$',register_views),
]

urlpatterns += [
    url(r'^check_uphone/$',check_uphone_views),
    url(r'^check_login/$',check_login_views),
    url(r'^logout/$',logout_views),
    url(r'^type_goods/$',type_goods_views),
    url(r'^add_cart/$',add_cart_views),
    url(r'^cart_count/$',cart_count_views),
]







