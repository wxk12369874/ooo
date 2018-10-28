from django.contrib import admin

# Register your models here.
from index.models import *

class GoodsAdmin(admin.ModelAdmin):
    list_filter = ('goodsType',)
    search_fields = ('title',)

admin.site.register(GoodsType)
admin.site.register(Goods,GoodsAdmin)
