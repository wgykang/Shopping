# from django.contrib import admin
from django.conf.urls import url, include
import xadmin
from study.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet, HotSearchsViewset
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet
from trade.views import ShopCarViewSet, OrderViewSet

router = DefaultRouter()
# 配置goods url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置category url
router.register(r'category', CategoryViewSet, base_name='category')
# 手机号注册验证码发送
router.register(r'codes', SmsCodeViewSet, base_name="codes")
# 热搜
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")
# 用户注册/修改获取用户信息
router.register(r'users', UserViewSet, base_name='users')
# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
# 用户留言
router.register(r'messages', LeavingMessageViewSet, base_name='messages')
# 用户收货地址
router.register(r'address', AddressViewSet, base_name='address')
# 购物车
router.register(r'shopcar', ShopCarViewSet, base_name='shopcar')
# 订单管理
router.register(r'orders', OrderViewSet, base_name='orders')
# 轮播图
router.register(r'banners', BannerViewSet, base_name='banners')
# 首页商品系列数据分类展示
router.register(r'indexgoods', IndexCategoryViewSet, base_name='indexgoods')

from trade.views import AliPayView

from django.views.generic import TemplateView

urlpatterns = [
    url('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^index/', TemplateView.as_view(template_name='index.html'), name='index'),
    # 商品列表页
    # url(r'good/', GoodsListView.as_view(), name='good-list'),
    url(r'docs/', include_docs_urls(title='Django练手项目')),
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    url(r'^login/$', obtain_jwt_token),   # 第三方登录也有login配加$符号,在django2.0不会出现这种情况
    # 支付宝支付接口
    url(r'^alipay/return/', AliPayView.as_view(), name='alipay'),
    # 第三方登录
    url('', include('social_django.urls', namespace='social'))

]
