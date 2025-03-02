from django.shortcuts import render
from django.http import JsonResponse  # ✅ JSON cavab üçün əlavə edildi
from .models import Tour, Booking
from .serializers import TourSerializer, BookingSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Yalnız adminlər üçün xüsusi icazə
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff  # ✅ `is_staff` yoxlanır

# ✅ **HTML səhifəsində turları göstərən View** (Frontend üçün)
def tour_list_html(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})

# ✅ **API üçün turların siyahısı (JSON qaytarır)**
def tour_list_json(request):
    tours = Tour.objects.all()
    serializer = TourSerializer(tours, many=True)
    return JsonResponse(serializer.data, safe=False)  # ✅ JSON cavab qaytarır

# ✅ Bütün turların siyahısını göstərmək üçün API View (Yalnız adminlər turlar əlavə edə bilər)
class TourListCreateView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]  # 🔐 Yalnız adminlər tur əlavə edə bilər
        return [IsAuthenticatedOrReadOnly()]  # ✅ Digərləri yalnız GET edə bilər

# ✅ Mövcud turu görmək, yeniləmək və silmək üçün API View
class TourDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [IsAdminUser()]  # 🔐 Yalnız adminlər dəyişiklik edə bilər
        return [IsAuthenticatedOrReadOnly()]  # ✅ Digərləri yalnız GET edə bilər

# ✅ Yeni rezervasiya yaratmaq və istifadəçinin rezervasiyalarını görmək
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # 🔐 Yalnız giriş etmiş istifadəçilər

    def perform_create(self, serializer):
        """ 🔹 Rezervasiya edərkən istifadəçinin öz məlumatlarını əlavə edir """
        serializer.save(user=self.request.user)

# ✅ Yalnız istifadəçinin öz rezervasiyalarını görməsi üçün API
class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # 🔐 Yalnız giriş etmiş istifadəçilər

    def get_queryset(self):
        """ 🔹 Yalnız cari istifadəçinin rezervasiyalarını qaytarır """
        return Booking.objects.filter(user=self.request.user)

# ✅ **Adminlər üçün bütün rezervasiyaları göstərən API**
class AdminBookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]  # 🔐 Yalnız adminlər görə bilər
