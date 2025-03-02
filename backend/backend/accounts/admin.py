from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Tour


# Xüsusi İstifadəçi modelinin idarə edilməsi
class CustomUserAdmin(UserAdmin):
    list_display = (
    'email', 'username', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'bonus')  # Görünən sütunlar
    search_fields = ('email', 'username')  # Axtarış imkanları
    ordering = ('email',)  # Email-ə görə sıralama
    filter_horizontal = ()  # İstədiyiniz əlaqəli sahələr varsa burada əlavə edə bilərsiniz.
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),  # Yeni admin statusu əlavə edirik
    )

    # `bonus` sahəsini model admininə əlavə etmək üçün:
    def bonus(self, obj):
        return obj.userprofile.bonus  # `UserProfile` modelindən bonus məlumatını qaytarır

    bonus.admin_order_field = 'userprofile__bonus'  # Admin paneldə sıralamağı təmin edir
    bonus.short_description = 'Bonus'  # Paneldə görünən ad


# İstifadəçi profilinin idarə edilməsi
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bonus')  # Görünəcək sahələr
    search_fields = ('user__username', 'user__email')  # İstifadəçi adına və email-ə görə axtarış
    ordering = ('user',)  # Profilə görə sıralama

    def bonus(self, obj):
        return obj.bonus  # Bonus qiymətini qaytarır

    bonus.admin_order_field = 'bonus'  # Admin paneldə sıralamağı təmin edir
    bonus.short_description = 'Bonus Miktarı'  # Paneldə görünən ad


# Tur modelinin idarə edilməsi
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'start_date', 'end_date')  # Görünən sütunlar
    search_fields = ('title', 'location')  # Axtarış funksiyası
    list_filter = ('start_date', 'end_date')  # Filtrləmə
    ordering = ('start_date',)  # Başlanğıc tarixinə görə sıralama

    def price(self, obj):
        return f"${obj.price}"  # Qiyməti formatlayıb göstərir

    price.admin_order_field = 'price'  # Admin paneldə qiymətə görə sıralama
    price.short_description = 'Price ($)'  # Paneldə görünən ad


# Adminə modelləri əlavə edirik
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tour, TourAdmin)
