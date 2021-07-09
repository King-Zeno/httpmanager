from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings

from utils.common import *

from manager.serializers.users import UserSerializer

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()


class UserViewSet(CustomListViewSet):
    """
    获取用户列表和用户详情
    """
    queryset = User.objects.filter(is_active=1).exclude(id=1)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)


class LoginView(JSONWebTokenAPIView):
    """
    用户登录
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            # 使用自定义的token用户信息
            payload = jwt_payload_handler(user)
            # token = serializer.object.get('token')
            token = jwt_encode_handler(payload)
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            
            return JsonResponse(code=200, data=response_data)
        return JsonResponse(code=401, msg=serializer.errors['non_field_errors'], status=status.HTTP_400_BAD_REQUEST)


# class UserMenuViewSet(CustomViewBase):
#     """
#     菜单管理
#     """
#     permission_classes = (permissions.IsAdminUser,)
#     serializer_class = UserMenuSerializer

#     queryset = Menu.objects.all()


# class GetUserMenuView(APIView):
#     """
#     用户获取菜单
#     """
#     # 将菜单平级数据转换为树级
#     def convert_json(self, data):
#         parent = []
#         children = []
#         new_data = []
#         for i in data:
#             if not i['parent']:
#                 parent.append(i)
#             else:
#                 children.append(i)

#         for i in parent:
#             i['list'] = []
#             for j in children:
#                 if j['parent'] == i['title']:
#                     i['list'].append(j)

#             new_data.append(i)

#         return new_data

#     def get(self, request, pk=None):
#         user = request.user
#         user_perm = UserSerializer(user).data['user_permissions']
        
#         if user.is_superuser:
#             queryset = Menu.objects.all()
#         else:
#             queryset = Menu.objects.filter(Q(perm_id=None) | Q(perm__in=user_perm))
#         data = ListMenuSerializer(queryset, many=True).data
#         new_data = self.convert_json(data)

#         return JsonResponse(code=200, msg="success", data=new_data)