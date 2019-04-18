from app import models


def template_area(request):
    # 获取升级行政区的地址
    return {'area': models.Area.objects.filter(area_type=1).all()}
