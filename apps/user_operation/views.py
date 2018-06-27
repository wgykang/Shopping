from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
   list:
       获取用户收藏列表
   retrieve:
       判断某个商品是否已经收藏
   create:
       收藏商品
   """
    # IsAuthenticated收藏时验证为当前登录用户，IsOwnerOrReadOnly删除收藏时验证权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # queryset = UserFav.objects.all() 获取全部用户的收藏列表
    # 局部验证token
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = UserFavSerializer
    lookup_field = "goods_id"

    # 回去当前的收藏列表，重载get_queryset方法
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer

    # 用户收藏后商品收藏数增加(也可以通过信号量完成signals,代码分离性较好)
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num += 1
    #     goods.save()


class LeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取留言
    create:
        添加留言
    delete:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


# class AddressViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                      viewsets.GenericViewSet):
class AddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址列表
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


