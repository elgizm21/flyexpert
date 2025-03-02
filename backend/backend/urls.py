from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.translation import gettext_lazy as _
import backend.accounts.views as account_views
from django.views.i18n import set_language

# ✅ Ana səhifə üçün sadə bir cavab qaytarır
def home_view(request):
    return HttpResponse(_("Welcome to the Tour Booking System!"))  # ✅ Çoxdillilik aktiv edildi

# ✅ Çoxdilli URL-lər
urlpatterns = [  # 🚀 **Burada `tuple` (`()`) yox, `list` (`[]`) istifadə et!**
    # ✅ Admin Panel
    path(_('admin/'), admin.site.urls),

    # ✅ İstifadəçi autentifikasiyası və qeydiyyatı URL-ləri
    path(_('api/accounts/register/'), account_views.UserRegisterView.as_view(), name='user_register'),
    path(_('api/accounts/login/'), account_views.UserLoginView.as_view(), name='user_login'),
    path(_('api/accounts/verify-email/'), account_views.VerifyEmailView.as_view(), name='verify_email'),
    path(_('api/accounts/user/'), account_views.UserProfileView.as_view(), name='user_profile'),

    # ✅ Bonus əlavə etmə
    path(_('api/accounts/add-bonus/'), account_views.AddBonusView.as_view(), name='add_bonus'),

    # ✅ Turlar və rezervasiyalar üçün API-lər
    path(_('api/tours/'), include('tours.urls')),  # 🔥 **Burada API `tours` üçün tam URL yazıldı**

    # ✅ Ana səhifə
    path('', home_view, name='home'),

    # ✅ JWT Token yaratmaq və yeniləmək
    path(_('api/token/'), TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(_('api/token/refresh/'), TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Dil dəyişdirmək üçün endpoint
    path('set-language/', set_language, name='set_language'),
]

# ✅ Media fayllarını göstərmək üçün URL konfiqurasiyası (yalnız DEBUG rejimində)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # ✅ Artıq TypeError olmayacaq
