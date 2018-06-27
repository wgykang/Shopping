# -*- coding: utf-8 -*- 
__author__ = 'yank'
__date__ = '2018/5/24/16:51'

from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Goods


class GoodsFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name='shop_price', help_text="最低价格", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='shop_price', help_text="最高价格", lookup_expr='lte')
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')  # 用SearchFilter替换
    top_category = filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'is_hot', 'is_new']
