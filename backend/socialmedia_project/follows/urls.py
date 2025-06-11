from rest_framework.routers import SimpleRouter

from .views import FollowViewSet

router = SimpleRouter()
router.register(r'', FollowViewSet)

urlpatterns = router.urls
