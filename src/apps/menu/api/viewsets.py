from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.menu.models import Menu
from .serializer import MenuSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    http_method_names = ['get',]
    permission_classes = [ IsAuthenticated ]
    

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params

        if params:
            code = params.get('code', None)
            if code:
                qs = qs.filter(code__startswith=code)

            level = params.get('level', None)
            if level:
                qs = qs.filter(level=level)

        return qs.order_by('code')