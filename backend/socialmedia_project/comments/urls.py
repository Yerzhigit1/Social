from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import CommentsViewSet
from likes.views import CommentLikeViewSet

router = SimpleRouter()
router.register(r'', CommentsViewSet, basename='comment')

urlpatterns = [
    path('toggle/', CommentLikeViewSet.as_view(), name='comment-like-toggle')
]

urlpatterns += router.urls
