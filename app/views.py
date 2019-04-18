from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import Q, F

from app import models


# Create your views here.

# 主页
def index(request):
    context = {
    }
    return render(request, 'app/index.html', context)


# 登陆
def acc_login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            return render(request, 'app/login.html', {'erro': "用户名或密码错误"})


# 注销
def acc_logout(request):
    logout(request)
    return render(request, 'app/index.html')


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'app/Register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        first_name = request.POST.get('first_name')
        area_id = request.POST.get('area')
        print(area_id)
        if all([username, email, phone, pwd1, pwd2, first_name, area_id]):
            if pwd1 != pwd2:
                return render(request, 'app/Register.html', {'erro': '两次输入密码不同！'})
            if models.User.objects.filter(username=username).first():
                return render(request, 'app/Register.html', {'erro': '当前用户名被占用！'})
            u = models.User.objects.create(username=username, email=email, first_name=first_name)
            u.set_password(pwd2)
            u.save()
            mu = models.MyUser.objects.create(user=u, phone=phone, area_id=area_id)
            return redirect('/login')
        return render(request, 'app/Register.html', {'erro': '注册失败,参数有误'})


# 新房列表页
@login_required
def new_house_list(request):
    house_obj = models.Houses.objects.filter(
        is_new=True,
        audit_type=3,
        area__in=request.user.myuser.area.area_set.all(),
    ).all()

    area_id = request.GET.get('area_id', '')
    if area_id:
        house_obj = house_obj.filter(area_id=area_id)

    area_name = request.GET.get('area_name', '')

    if area_name:
        house_obj = house_obj.filter(area__name=area_name)

    price = request.GET.get('price', '')
    if price:
        price_list = [float(i) for i in price.split(',')]
        house_obj = house_obj.filter(Q(price__gte=price_list[0]), Q(price__lte=price_list[1]))

    door_model = request.GET.get('door_model', '')
    if door_model:
        house_obj = house_obj.filter(door_model=int(door_model))

    house_type = request.GET.get('house_type', '')
    if house_type:
        house_obj = house_obj.filter(house_type=int(house_type))

    title = request.GET.get('title')
    if title:
        house_obj = house_obj.filter(title__contains=title)

    filter_data = {
        'area_id': area_id,
        'price': price,
        'door_model': door_model,
        'house_type': house_type,
        'area_name': area_name

    }
    context = {
        'house_obj': house_obj,
        'filter_data': filter_data
    }
    return render(request, 'app/house_list.html', context)


# 二手房列表页
@login_required
def old_house_list(request):
    house_obj = models.Houses.objects.filter(
        is_new=False,
        audit_type=3,
        area__in=request.user.myuser.area.area_set.all(),
    ).all()

    area_id = request.GET.get('area_id', '')
    if area_id:
        house_obj = house_obj.filter(area_id=area_id)

    price = request.GET.get('price', '')
    if price:
        price_list = [float(i) for i in price.split(',')]
        house_obj = house_obj.filter(Q(price__gte=price_list[0]), Q(price__lte=price_list[1]))

    door_model = request.GET.get('door_model', '')
    if door_model:
        house_obj = house_obj.filter(door_model=int(door_model))

    house_type = request.GET.get('house_type', '')
    if house_type:
        house_obj = house_obj.filter(house_type=int(house_type))

    filter_data = {
        'area_id': area_id,
        'price': price,
        'door_model': door_model,
        'house_type': house_type

    }
    context = {
        'house_obj': house_obj,
        'filter_data': filter_data
    }
    return render(request, 'app/house_list.html', context)


# 房屋详情页
@login_required
def house_detail(request, houseid):
    house_obj = models.Houses.objects.filter(pk=houseid).first()
    # 创建一个浏览历史记录
    if not models.BrowsingHistory.objects.filter(user=request.user, house=house_obj):
        models.BrowsingHistory.objects.create(user=request.user, house=house_obj)

    is_interview = False
    # 是否申请面谈
    interview_obj = models.Interview.objects.filter(user=request.user, house=house_obj).first()
    if interview_obj:
        is_interview = interview_obj.is_pass
    context = {
        'house_obj': house_obj,
        'is_interview': is_interview
    }
    return render(request, 'app/HouseDetail.html', context)


# 用户更新所属区域
@login_required
def update_area(request):
    area_id = request.POST.get('areaID')
    area_obj = models.Area.objects.filter(pk=area_id).first()
    if area_obj:
        user = models.MyUser.objects.filter(user=request.user).first()
        if user:
            user.area = area_obj
            user.save()
            return JsonResponse({'status': True})
    return JsonResponse({'status': False})


# 个人发布的房屋管理
def manage_release(request):
    house_obj = models.Houses.objects.filter(user=request.user).all()

    context = {
        'house_obj': house_obj
    }
    return render(request, 'userinfo/ManageRelease.html', context)


# 修改个人信息
@login_required
def change_user_info(request):
    if request.method == 'GET':
        return render(request, 'userinfo/changeUserInfo.html')
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if all([first_name, email, phone]):
            user = request.user
            user.first_name = first_name
            user.email = email
            user.save()
            myuser = user.myuser
            myuser.phone = phone
            myuser.save()
            return render(request, 'userinfo/changeUserInfo.html')


# 修改个人密码
@login_required
def change_password(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'userinfo/changePassword.html')
    elif request.method == 'POST':
        oldpassword = request.POST.get('oldpassword')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        if all([oldpassword, pwd1, pwd2]):
            if pwd1 == pwd2:
                user = request.user
                user.set_password(pwd2.strip())
                user.save()
                return redirect('/login')


# 个人浏览历史记录
@login_required
def show_history(request):
    histery_obj = models.BrowsingHistory.objects.filter(user=request.user)
    return render(request, 'userinfo/ShowHistory.html', {'histery_obj': histery_obj})


# 面谈管理
@login_required
def show_interview(request):
    house = models.Houses.objects.filter(user=request.user)
    interview_obj = models.Interview.objects.filter(house__in=house)
    context = {
        'interview_obj': interview_obj
    }
    return render(request, 'userinfo/ShowInterview.html', context)


# 审核发布
@login_required
def audit(request):
    house_obj_list = models.Houses.objects.filter(audit_type=1)
    context = {
        'house_obj_list': house_obj_list
    }
    return render(request, 'userinfo/audit.html', context)


# 发布新房屋
@login_required
def add_house(request):
    if request.method == 'GET':
        return render(request, 'userinfo/addHouse.html')
    title = request.POST.get('title')  # title
    area_id = request.POST.get('area')  # 区域
    plot_nanme = request.POST.get('plot_name')  # 小区名称
    acreage = request.POST.get('acreage')  # 面积
    price = request.POST.get('price')  # 单价
    total_prices = request.POST.get('total_prices')  # 总价
    door_model = request.POST.get('door_model')  # 户型
    house_type = request.POST.get('house_type')  # 房屋类型
    is_new = bool(request.POST.get('is_new'))
    decorate_situation = request.POST.get('decorate_situation')
    fllor = request.POST.get('fllor')
    master_img = request.FILES.get('master_img')
    img = request.FILES.getlist('img')
    housing_details = request.POST.get('housing_details')

    # 开始创建一个房屋

    house_obj = models.Houses()
    house_obj.title = title
    house_obj.is_new = is_new
    house_obj.area_id = int(area_id)
    house_obj.plot_name = plot_nanme
    house_obj.acreage = int(acreage)
    house_obj.price = float(price)
    house_obj.total_prices = float(total_prices)
    house_obj.housing_details = housing_details
    house_obj.door_model = int(door_model)
    house_obj.house_type = int(house_type)
    house_obj.fllor = int(fllor)
    if request.user.is_staff:
        house_obj.audit_type = 3
    else:
        house_obj.audit_type = 1
    house_obj.decorate_situation = decorate_situation
    house_obj.user = request.user

    house_obj.save()
    house_obj.master_img.save(master_img.name, master_img)

    for i in img:
        obj = models.HouseImg()
        obj.img.save(i.name, i)
        obj.save()
        house_obj.img.add(obj.id)
    house_obj.save()

    return redirect('/ManageRelease')


# 主页搜索跳转
@login_required
def search(request):
    print(request.POST)
    if request.method == 'POST':
        area_name = request.POST.get('area_name')
        url = request.POST.get('url')
        price = request.POST.get('price')
        title = request.POST.get('title')
        return redirect('%s?title=%s&area_name=%s&price=%s' % (url, title, area_name, price))


# 申请面谈
def sqmt(request):
    house_id = request.POST.get('houseID')
    if not models.Interview.objects.filter(user=request.user, house_id=house_id):
        models.Interview.objects.create(user=request.user, house_id=house_id)
    return JsonResponse({'status': True})


# 同意面谈
def tymt(request):
    interview_id = request.POST.get('interviewID')
    interciew_obj = models.Interview.objects.filter(pk=interview_id)
    if interciew_obj:
        interciew_obj.update(is_pass=True)
        return JsonResponse({'status': True})


# 发布房屋通过
def shtg(request):
    house_id = request.POST.get('houseID')
    house_obj = models.Houses.objects.filter(pk=house_id).first()
    if house_obj and request.user.is_staff:
        house_obj.audit_type = 3
        house_obj.save()
        return JsonResponse({"status": True})
