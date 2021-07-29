from utils.common import CustomViewBase, JsonResponse
from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from manager.models.api import Api
from manager.serializers.api import ApiSerializer


class ApiViewSet(CustomViewBase):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        username = "%s%s" % (request.user.last_name, request.user.first_name)
        data = request.data
        data['author'] = username

        serializer = self.get_serializer(data=data)
        is_valid = serializer.is_valid(raise_exception=True)
        if not is_valid:
            return JsonResponse(code=400, msg=serializer.errors)

        self.perform_create(serializer)
        return JsonResponse(code=200, msg="success", data=serializer.data)
