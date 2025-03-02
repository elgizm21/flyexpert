from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    jwt_test_view,
    UserRegisterView,
    VerifyEmailView,  # ✅ Yeni Email Təsdiqləmə API-si əlavə edildi
    protected_view,
    UserProfileView,
    get_csrf_token,
    CustomUserLogoutView
)

urlpatterns = [
    path('jwt-test/', jwt_test_view, name='jwt_test'),  # ✅ JWT test
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Token yaratmaq
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # ✅ Token yeniləmək
    path('register/', UserRegisterView.as_view(), name='user_register'),  # ✅ İstifadəçi qeydiyyatı
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),  # ✅ Email təsdiqləmə üçün yeni API
    path('protected-view/', protected_view, name='protected_view'),  # ✅ Qorunan səhifə
    path('user/', UserProfileView.as_view(), name='user_profile'),  # ✅ İstifadəçi profili
    path('csrf/', get_csrf_token, name='get_csrf_token'),  # ✅ CSRF token endpointi
    path('api/token/logout/', CustomUserLogoutView.as_view(), name='token_logout'),  # ✅ Logout endpointi
]
