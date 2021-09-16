from rest_framework import routers
from .viewsets import MenuViewSet

router = routers.DefaultRouter()
router.register(r'menus', MenuViewSet)

urlpatterns = router.urls