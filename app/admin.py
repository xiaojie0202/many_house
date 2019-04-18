from django.contrib import admin
from app import models


# Register your models here.

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'province']


@admin.register(models.MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Houses)
class HousesAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    filter_horizontal = ['img']


@admin.register(models.HouseImg)
class HouseImgAdmin(admin.ModelAdmin):
    pass
