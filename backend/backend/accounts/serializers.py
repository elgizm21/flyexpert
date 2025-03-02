from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Yeni istifadəçi qeydiyyatı üçün serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'email', 'is_superuser']  # 🔹 `is_superuser` əlavə edildi

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """
        Yeni istifadəçi yaradarkən `set_password` metodundan istifadə edirik ki, parol `hash` edilsin.
        """
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # ✅ Parolu təhlükəsiz şəkildə hash edir
        user.is_active = False  # 🔹 İstifadəçi email təsdiqləyənə qədər deaktiv qalsın
        user.save()  # ✅ İstifadəçini bazaya əlavə edir
        return user

# ✅ İstifadəçi profilini göstərmək və redaktə etmək üçün serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ✅ Email təsdiqləmə üçün serializer
class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
