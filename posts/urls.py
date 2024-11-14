from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, PublishUnpublishPostView, LikeUnlikeView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'users', UserViewSet,basename='users')
router.register(r'posts', PostViewSet,basename='posts')
router.register(r'publish', PublishUnpublishPostView, basename='publish')
router.register(r'like', LikeUnlikeView, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
