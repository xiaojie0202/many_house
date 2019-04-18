from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 地区表
class Area(models.Model):
    area_type_choices = (
        (1, '省'),
        (2, '市'),
        (3, '区/县')
    )
    name = models.CharField(max_length=10, verbose_name='地区名称')
    area_type = models.PositiveIntegerField(choices=area_type_choices, verbose_name='行政级别')
    province = models.ForeignKey(to='Area', verbose_name='所属省会', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


# 用户扩展表
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    phone = models.CharField(max_length=28, verbose_name='手机号')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='用户所属地区')

    def __str__(self):
        return self.user.first_name


# 图片表
class HouseImg(models.Model):
    img = models.ImageField(upload_to='housesImg', verbose_name='图片')


# 房屋表
class Houses(models.Model):
    door_model_choices = (
        (1, '一室'),
        (2, '二室'),
        (3, '三室'),
        (4, '四室'),
        (5, '四室以上')
    )
    house_type_choices = (
        (1, '住宅'),
        (2, '别墅'),
        (3, '写字楼'),
        (4, '商铺')
    )
    audit_type_choices = (
        (1, '待审核'),
        (2, '审核失败'),
        (3, '审核通过')
    )
    title = models.CharField(max_length=128, verbose_name='房屋标题')
    area = models.ForeignKey('Area', on_delete=models.CASCADE, verbose_name='所属区域')
    plot_name = models.CharField(max_length=64, verbose_name='所属小区名')
    acreage = models.PositiveIntegerField(verbose_name='面积')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格(元/m)')
    total_prices = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价(万)')
    housing_details = models.TextField(verbose_name='房屋详情')
    door_model = models.PositiveIntegerField(choices=door_model_choices, verbose_name='户型')
    house_type = models.PositiveIntegerField(choices=house_type_choices, verbose_name='房屋类型')
    is_new = models.BooleanField(verbose_name='是否是新房')
    master_img = models.ImageField(upload_to='houseImg', verbose_name='房屋主图')
    img = models.ManyToManyField(to='HouseImg', verbose_name='房屋图片')
    fllor = models.PositiveIntegerField(verbose_name='楼层')
    audit_type = models.PositiveIntegerField(choices=audit_type_choices, verbose_name='审核状态')
    user = models.ForeignKey(User, verbose_name='发布用户', on_delete=models.CASCADE)
    decorate_situation = models.CharField(max_length=12, verbose_name='装修情况')
    create_datetime = models.DateTimeField(auto_now=True, verbose_name='发布时间')

    def __str__(self):
        return self.title


# 申请面谈表
class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(Houses, on_delete=models.CASCADE, verbose_name='申请面谈房屋')
    is_pass = models.BooleanField(default=False, verbose_name='申请通过')

    def __str__(self):
        return self.house.title


# 浏览历史表
class BrowsingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(Houses, on_delete=models.CASCADE, verbose_name='申请面谈房屋')
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.house.title
