from django.shortcuts import redirect
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ShopCarSerializer, ShopCarDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.permissions import IsOwnerOrReadOnly


class ShopCarViewSet(viewsets.ModelViewSet):
    """
    用户购物车
    list:
        获取购物车商品列表
    create:
        添加购物车
    update:
        更新购物车商品数量
    delete:
        删除购物车
    """
    serializer_class = ShopCarSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    # 当前用户的购物车列表
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCarDetailSerializer
        else:
            return ShopCarSerializer

    # 增加购物车商品库存数减少
    def perform_create(self, serializer):
        shop_car = serializer.save()
        goods = shop_car.goods
        goods.goods_num -= shop_car.nums
        goods.save()

    # 删除购物车商品时库存数增加
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()

    # 修改购物车数量,商品库存改变
    def perform_update(self, serializer):
        # 修改之前的库存数量
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        # 变化的数量,修改后的数量减去修改前的数量
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


# 订单不允许修改,不使用update
class OrderViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    """
    订单管理
    list:
        获取当前用户订单
    create:
        创建订单
    delete:
        删除订单
    """
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 当前用户的订单列表
    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 在订单提交保存之前还需要多两步步骤，所以这里自定义perform_create方法
    # 1.将购物车中的商品保存到OrderGoods中
    # 2.清空购物车
    def perform_create(self, serializer):
        order = serializer.save()
        # 获取购物车所有商品
        shop_cars = ShoppingCart.objects.filter(user=self.request.user)
        for shop_car in shop_cars:
            order_goods = OrderGoods()
            order_goods.goods = shop_car.goods
            order_goods.goods_num = shop_car.nums
            order_goods.order = order
            order_goods.save()
            shop_car.delete()
        return order

    # 动态配置Serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer


from study.settings import private_key_path, ali_pub_key_path
from utils.alipay import AliPay
from rest_framework.response import Response
from datetime import datetime


# 跟支付宝相关,没有model,使用最底层apiview
class AliPayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        """
        processed_dict = {}
        # 1. 获取GET中参数
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 2. 取出sign
        sign = processed_dict.pop("sign", None)

        # 3. 生成ALipay对象
        alipay = AliPay(
            appid="2016091400506463",
            app_notify_url="http://203.195.162.142/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://203.195.162.142:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            # trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

                # response = redirect("index")
                # response.set_cookie("nextPath", "pay", max_age=3)
            response = redirect("/index/#/app/home/member/order")
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        """
        # 存放post里面所有的数据
        processed_dict = {}
        # 取出post里面的数据
        for key, value in request.POST.items():
            processed_dict[key] = value
        # 把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)

        # 生成一个Alipay对象
        alipay = AliPay(
            appid="2016091400506463",
            app_notify_url="http://203.195.162.142/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://203.195.162.142/alipay/return/"
        )

        # 进行验证
        verify_re = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_re is True:
            # 商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)
            # 支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            # 交易状态
            trade_status = processed_dict.get('trade_status', None)

            # 查询数据库中订单记录
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response("success")
