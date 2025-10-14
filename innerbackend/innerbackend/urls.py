from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import MeView, UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path
from api.views import MyTokenObtainPairView, ChangePasswordView, UpdateProfileView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/me/", MeView.as_view(), name="me"),
    path("api/", include(router.urls)),
    path('inventory/', include('inventory.urls')),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("update-profile/", UpdateProfileView.as_view(), name="update-profile"),
    path('menu/', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)