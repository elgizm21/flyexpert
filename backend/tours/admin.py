from django.contrib import admin
from .models import Tour, Booking


# ✅ **Turları admin paneldə idarə etmək üçün ModelAdmin**
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'available_seats', 'start_date', 'end_date', 'created_at')
    search_fields = ('title', 'location')
    list_filter = ('start_date', 'end_date')
    list_editable = ('available_seats',)  # 🔹 Mövcud yerləri admin paneldən redaktə etmək imkanı
    ordering = ('-created_at',)  # 🔹 Yeni turlar ilk görünsün


# ✅ **Rezervasiyaları admin paneldə idarə etmək üçün ModelAdmin**
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'num_seats', 'status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('user__email', 'tour__title')  # 🔹 İstifadəçi emaili və tur adına görə axtarış
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')  # 🔹 Filtr imkanı
    list_editable = ('status', 'payment_status')  # 🔹 Admin paneldə statusu dəyişmək imkanı
    ordering = ('-created_at',)  # 🔹 Yeni rezervasiyalar ilk görünsün
