from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PostViewSet

router = DefaultRouter()
router.register(r'', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:post_id>/like/', include('likes.urls')),
    path('<int:post_id>/comments/', include('comments.urls'))
]