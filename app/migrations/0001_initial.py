# Generated by Django 2.1.5 on 2019-04-16 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='地区名称')),
                ('area_type', models.PositiveIntegerField(choices=[(1, '省'), (2, '市'), (3, '区/县')], verbose_name='行政级别')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Area', verbose_name='所属省会')),
            ],
        ),
        migrations.CreateModel(
            name='BrowsingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HouseImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='housesImg', verbose_name='图片')),
            ],
        ),
        migrations.CreateModel(
            name='Houses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='房屋标题')),
                ('plot_name', models.CharField(max_length=64, verbose_name='所属小区名')),
                ('acreage', models.PositiveIntegerField(verbose_name='面积')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格(元/m)')),
                ('total_prices', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='总价(万)')),
                ('housing_details', models.TextField(verbose_name='房屋详情')),
                ('door_model', models.PositiveIntegerField(choices=[(1, '一室'), (2, '二室'), (3, '三室'), (4, '四室'), (5, '四室以上')], verbose_name='户型')),
                ('house_type', models.PositiveIntegerField(choices=[(1, '住宅'), (2, '别墅'), (3, '写字楼'), (4, '商铺')], verbose_name='房屋类型')),
                ('is_new', models.BooleanField(verbose_name='是否是新房')),
                ('master_img', models.ImageField(upload_to='houseImg', verbose_name='房屋主图')),
                ('fllor', models.PositiveIntegerField(verbose_name='楼层')),
                ('audit_type', models.PositiveIntegerField(choices=[(1, '审核中'), (2, '审核失败'), (3, '审核通过')], verbose_name='审核状态')),
                ('decorate_situation', models.CharField(max_length=12, verbose_name='装修情况')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Area', verbose_name='所属区域')),
                ('img', models.ManyToManyField(to='app.HouseImg', verbose_name='房屋图片')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布用户')),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_pass', models.BooleanField(default=False, verbose_name='申请通过')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Houses', verbose_name='申请面谈房屋')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=28, verbose_name='手机号')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Area', verbose_name='用户所属地区')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.AddField(
            model_name='browsinghistory',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Houses', verbose_name='申请面谈房屋'),
        ),
        migrations.AddField(
            model_name='browsinghistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
