# -*- coding: utf-8 -*-
__author__ = 'yank'
__date__ = '2018/5/23/19:24'

from rest_framework import serializers
from django.db.models import Q

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd, HotSearchWords


# 三类category
class GoodsCategorySerializerThree(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 二类category
class GoodsCategorySerializerSecond(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializerThree(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 一类category
class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializerSecond(many=True)  # 有多个子类

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImgSerializer(many=True)

    class Meta:
        model = Goods
        # 取部分 fields = ('字段名')
        # 取所有
        fields = '__all__'


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


# 首页商品分类显示
class IndexSerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializerSecond(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    class Meta:
        model = GoodsCategory
        fields = '__all__'
