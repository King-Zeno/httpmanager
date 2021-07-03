
from django.urls import path
from django.urls import re_path
from django.conf.urls import url, include
from manager.views import users
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter() # 只需要实现一次
router.register(r'', users.UserViewSet, basename='users')


urlpatterns = [
    path('login/',users.LoginView.as_view(),name='login'),
    # path('get_menu/', users.GetUserMenuView.as_view(), name='get_menu'),
    re_path('^', include(router.urls)),
]
