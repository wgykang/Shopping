from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework_extensions.cache.mixins import CacheResponseMixin  # def缓存
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle  # 限速访问

from .filters import GoodsFilter
from .models import Goods, GoodsCategory, Banner, HotSearchWords
from goods.serializers import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, IndexSerializer, \
    HotWordsSerializer


# 分页
class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# CacheResponseMixin放在第一个类继承
class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    商品列表页，分页，搜索，过滤
    retrieve:
    获取商品详情
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)  # 限速
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, )   # 需要验证时候使用，不需全局配置
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')  # 搜索
    ordering_fields = ('sold_num', 'shop_price')  # 排序

    # 商品点击数自动修改
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    商品分类列表数据
    retrieve:
    获得商品详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by('-index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品首页分类展示
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料", '粮油副食'])
    serializer_class = IndexSerializer
