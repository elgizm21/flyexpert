from django.core.mail import send_mail
from rest_framework import status
from django.utils.crypto import get_random_string
from .serializers import UserRegisterSerializer, EmailVerificationSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken, RefreshToken
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import ensure_csrf_cookie


User = get_user_model()

# 🔹 Müvəqqəti olaraq təsdiq kodlarını saxlamaq üçün (real sistemdə DB istifadə edilməlidir)
verification_codes = {}


# ✅ **Test view – API-nin işlədiyini yoxlamaq üçün**
@api_view(['GET'])
def jwt_test_view(request):
    return Response({"message": "JWT is working!"})


# ✅ **İstifadəçi Qeydiyyatı + Email təsdiqləmə kodu göndərilməsi**
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 🔹 6 rəqəmli təsdiq kodu yarat
            verification_code = get_random_string(length=6, allowed_chars='1234567890')
            verification_codes[user.email] = verification_code

            # 🔹 Email göndər
            send_mail(
                'Email Təsdiqləmə Kodu',
                f'Sizin təsdiq kodunuz: {verification_code}',
                'your_email@example.com',  # 🔹 Burada real emailini qeyd et
                [user.email],
                fail_silently=False,
            )

            # 🔹 Bonus əlavə et
            user.bonus = 10  # 10 bonus əlavə et
            user.save()  # Bonus məlumatını qeydiyyatdan sonra istifadəçiyə əlavə et

            return Response({'message': 'Təsdiq kodu emailə göndərildi. Bonus əlavə olundu.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ **İstifadəçi Login API**
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # İstifadəçi autentifikasiyası
        user = authenticate(username=username, password=password)
        if user is not None:
            # Token yaratmaq
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_admin': user.is_superuser,  # Admin olub-olmadığını göndərir
                'username': user.username,
                'email': user.email
            })
        return Response({'error': 'İstifadəçi adı və ya şifrə yanlışdır'}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ **Email Təsdiqləmə API-si**
class VerifyEmailView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            if email in verification_codes and verification_codes[email] == code:
                try:
                    user = User.objects.get(email=email)
                    user.is_active = True  # 🔹 İstifadəçini aktiv et
                    user.save()
                    del verification_codes[email]  # 🔹 Kod siyahıdan silinsin
                    return Response({'message': 'Email təsdiqləndi, indi daxil ola bilərsiniz.'},
                                    status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'message': 'İstifadəçi tapılmadı.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Yanlış kod.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ **İstifadəçi Profil API (Profil məlumatlarını göstərmək və yeniləmək üçün)**
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # 🔹 Cari istifadəçinin məlumatlarını qaytarır


# ✅ **Qorunan API (Yalnız token ilə giriş mümkündür)**
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "Bu qorunan səhifədir!"})


# ✅ **CSRF token endpointi**
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"csrfToken": request.META.get("CSRF_COOKIE", "")})


# ✅ **Custom Logout View – İstifadəçini logout edən API**
class CustomUserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 🔹 İstifadəçinin bütün aktiv tokenlərini blackliste sal
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# ✅ **User Bonusları - Bonus verilməsi**
class AddBonusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            bonus_amount = request.data.get('bonus_amount', 10)  # Bonus məbləğini parametrlə alırıq (default 10)

            # İstifadəçiyə bonus əlavə et
            user.bonus += bonus_amount
            user.save()

            return Response({'message': f'{bonus_amount} bonus əlavə olundu.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
