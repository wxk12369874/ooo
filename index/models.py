from django.db import models

# Create your models here.
class Users(models.Model):
    uphone = models.CharField(max_length=20,verbose_name='电话号码')
    upwd = models.CharField(max_length=20,verbose_name='密码')
    uemail = models.EmailField(verbose_name='电子邮件')
    uname = models.CharField(max_length=20,verbose_name='用户名')
    isActive = models.BooleanField(default=True,verbose_name='是否激活')

    def __str__(self):
        return self.uphone

    def to_dict(self):
        dic = {
            "id" : self.id,
            "uphone":self.uphone,
            "upwd" : self.upwd,
            "uname" : self.uname,
            "uemail" : self.uemail,
            "isActive": self.isActive
        }
        return dic

# 创建商品类型的实体 - GoodsType
class GoodsType(models.Model):
    # 商品类型名称
    title = models.CharField(max_length=50,verbose_name='类型名称')
    # 商品类型图片
    picture = models.ImageField(upload_to='static/upload/goodstype',null=True,verbose_name='类型图片')
    # 商品类型描述
    desc=models.TextField(verbose_name='商品描述')

    def __str__(self):
        return self.title

    def to_dict(self):
        dic = {
            'title':self.title,
            'picture':self.picture.__str__(),
            'desc':self.desc,
        }
        return dic

    class Meta:
        db_table='GoodsType'
        verbose_name='商品类型'
        verbose_name_plural=verbose_name

class Goods(models.Model):
    title=models.CharField(max_length=40,verbose_name='商品名称')
    price=models.DecimalField(max_digits=7,decimal_places=2,verbose_name='商品价格')
    spec=models.CharField(max_length=30,verbose_name='规格')
    picture=models.ImageField(upload_to='static/upload/goods',null=True,verbose_name='商品图片')
    goodsType=models.ForeignKey(GoodsType,verbose_name='商品类型')
    isActive=models.BooleanField(default=True,verbose_name='是否上架')

    def __str__(self):
        return self.title

    class Meta:
        db_table="Goods"
        verbose_name="商品"
        verbose_name_plural=verbose_name

# 购物车实体
class CartInfo(models.Model):
    users = models.ForeignKey(Users,db_column='users_id',verbose_name='用户')
    goods = models.ForeignKey(Goods,db_column='goods_id',verbose_name='商品')
    ccount= models.IntegerField(verbose_name='购买数量')

    def __str__(self):
        return self.ccount

    class Meta:
        db_table="CartInfo"







