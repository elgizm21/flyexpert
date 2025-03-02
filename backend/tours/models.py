from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# ✅ Tur Modeli (Turların məlumatları)
class Tour(models.Model):
    title = models.CharField(max_length=255)  # 🟢 Turun adı
    description = models.TextField()  # 🟢 Açıqlama
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 🟢 Qiymət
    image = models.ImageField(upload_to='tours/', blank=True, null=True)  # 🟢 Şəkil
    available_seats = models.PositiveIntegerField(default=0)  # 🟢 Mövcud yerlər
    start_date = models.DateField()  # 🟢 Başlama tarixi
    end_date = models.DateField()  # 🟢 Bitmə tarixi
    location = models.CharField(max_length=255)  # 🟢 Məkan
    created_at = models.DateTimeField(auto_now_add=True)  # 🟢 Yaradılma tarixi

    class Meta:
        ordering = ['-created_at']  # Yeni əlavə olunan turlar ilk göstərilsin

    def __str__(self):
        return f"{self.title} - {self.location}"

# ✅ Rezervasiya Modeli
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),  # 🔹 Gözləmə
        ("confirmed", "Confirmed"),  # 🔹 Təsdiqlənmiş
        ("cancelled", "Cancelled"),  # 🔹 Ləğv olunmuş
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),  # 🔹 Ödəniş gözlənilir
        ("paid", "Paid"),  # 🔹 Ödənilib
        ("failed", "Failed"),  # 🔹 Uğursuz ödəniş
    ]

    PAYMENT_METHOD_CHOICES = [
        ("card", "Card"),  # 🔹 Kartla ödəniş (Stripe və ya bank kartı)
        ("transfer", "Bank Transfer"),  # 🔹 Bank köçürməsi
        ("cash", "Cash Payment"),  # 🔹 Nağd ödəniş
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🟢 İstifadəçi (Rezervasiya edən)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)  # 🟢 Hansi tura rezervasiya edildiyi
    num_seats = models.PositiveIntegerField()  # 🟢 Rezervasiya edilən yerlərin sayı
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")  # 🟢 Rezervasiya statusu
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending")  # 🟢 Ödəniş statusu
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, default="card")  # 🟢 Ödəniş metodu
    created_at = models.DateTimeField(auto_now_add=True)  # 🟢 Yaradılma tarixi

    class Meta:
        ordering = ['-created_at']  # Ən son rezervasiyalar yuxarıda olsun

    def __str__(self):
        return f"{self.user.email} - {self.tour.title} ({self.num_seats} seats)"

    # ✅ Mövcud yerlərin azaldılması (avtomatik yoxlama)
    def save(self, *args, **kwargs):
        if self.pk is None:  # Yalnız yeni rezervasiyalarda işləsin
            if self.tour.available_seats < self.num_seats:
                raise ValidationError("Bu tur üçün kifayət qədər yer yoxdur!")
            self.tour.available_seats -= self.num_seats  # 🟢 Yer azaldılır
            self.tour.save()

        super().save(*args, **kwargs)
