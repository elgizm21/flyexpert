from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


# ✅ İstifadəçi Meneceri (Admin və Normal İstifadəçiləri yaratmaq üçün)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("İstifadəçinin emaili olmalıdır")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


# ✅ **Xüsusi İstifadəçi Modeli**
class CustomUser(AbstractUser):  # 🚀 DÜZƏLDİM (Artıq AbstractUser-dən miras alır)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Email ilə giriş
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email  # Admin paneldə email göstərilir


# ✅ **İstifadəçi Profil Modeli**
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Hər istifadəçiyə bir profil
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Bonus

    def __str__(self):
        return f"Profile for {self.user.username}"

    def add_bonus(self, amount):
        """Bonus əlavə etmək üçün funksiya"""
        self.bonus += amount
        self.save()


# ✅ **İstifadəçi qeydiyyatında bonus əlavə etmək**
def post_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Yeni istifadəçi qeydiyyatı zamanı bonus əlavə etmək
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.add_bonus(10)  # 10 bonus əlavə et
        user_profile.save()


# ✅ **Hər yeni istifadəçi yaradıldıqda profil yaratmaq**
models.signals.post_save.connect(post_save_user_profile, sender=CustomUser)


# ✅ **Tur Modeli**
class Tour(models.Model):
    title = models.CharField(max_length=255)  # Turun adı
    description = models.TextField()  # Açıqlama
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Qiymət
    image = models.ImageField(upload_to='tours/', blank=True, null=True)  # Şəkil
    available_seats = models.IntegerField(default=0)  # Mövcud yerlər
    start_date = models.DateField()  # Başlama tarixi
    end_date = models.DateField()  # Bitmə tarixi
    location = models.CharField(max_length=255)  # Məkan
    created_at = models.DateTimeField(auto_now_add=True)  # Yaradılma tarixi

    def __str__(self):
        return self.title  # Admin paneldə turun adı göstərilir
