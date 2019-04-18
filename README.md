# 多多房 房产交易网站
# 开发环境
    python3.7

# 依赖库
    pip install Django==2.1.5
    pip install Pillow==6.0.0
    pip install PyMySQL==0.9.3

# 更换数据库为mysql
>- settings.py
```
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': '数据库名字',
#         'USER': '数据库用户名',
#         'PASSWORD': '数据库密码',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }
```

>- app/__init__.py
```python
import pymysql
pymysql.install_as_MySQLdb()
```

# 运行
    python manage.py runserver
    
# 项目截图
![](https://github.com/xiaojie0202/many_house/blob/master/media/%E6%88%AA%E5%9B%BE1.png)
![](https://github.com/xiaojie0202/many_house/blob/master/media/%E6%88%AA%E5%9B%BE2.png)
![](https://github.com/xiaojie0202/many_house/blob/master/media/%E6%88%AA%E5%9B%BE3.png)