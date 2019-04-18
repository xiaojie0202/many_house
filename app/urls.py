from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),  # 主页
    path('login', views.acc_login, name='login'),  # 登录页
    path('register', views.register, name='register'),  # 注册页
    path('logout', views.acc_logout, name='logout'),  # 注销
    path('NewHouseList', views.new_house_list, name='new_house_list'),  # 新房列表
    path('OldHouseList', views.old_house_list, name='old_house_list'),  # 二手房列表
    path('HouseDetail/<int:houseid>', views.house_detail, name='house_detail'),  # 房屋详情页
    path('updateArea', views.update_area),  # 更新用户所属地址

    # 用户信息相关
    path('changeUserInfo', views.change_user_info, name='changeUserInfo'),  # 修改个人信息
    path('changePassword', views.change_password),  # 修改密码
    path('ManageRelease', views.manage_release, name='manage_release'),  # 个人发布管理
    path('ShowHistory', views.show_history),  # 浏览历史
    path('ShowInterview', views.show_interview), # 面谈管理
    path('audit', views.audit),  # 审核发布
    path('addHouse', views.add_house),  # 发布新房昂无
    path('search', views.search),  # 搜索跳转
    path('sqmt', views.sqmt), # 申请面谈
    path('tymt', views.tymt), # 申请面谈
    path('shtg', views.shtg), # 申请面谈
]
