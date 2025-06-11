from .views import LikesViewSet
from django.urls import path

like_view = LikesViewSet.as_view({
    'post': 'create',
    'delete': 'destroy'
})

urlpatterns = [
    path('', like_view, name='like')
]
