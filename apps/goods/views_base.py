import json

from django.http import HttpResponse
from django.views.generic.base import View
# from django.views.generic import ListView
from goods.models import Goods


# class GoodsListView(View):
#     def get(self, request):
#         json_list = []
#         goods = Goods.objects.all()[:10]
#         for good in goods:
#             json_dict = {}
#             json_dict['name'] = good.name
#             json_dict['category'] = good.category.name
#             json_dict['market_price'] = good.market_price
#             json_list.append(json_dict)
#         return HttpResponse(json.dumps(json_list), content_type='Application/json')

# model_to_dict无法将ImageFieldFile和DatetimeField序列化
class GoodsListView(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]
        # for good in goods:
        #     from django.forms import model_to_dict
        #     json_list.append(model_to_dict(good))
        # return HttpResponse(json.dumps(json_list), content_type='Application/json')
        from django.core import serializers
        from django.http import JsonResponse
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)