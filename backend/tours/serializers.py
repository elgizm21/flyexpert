from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Tour, Booking

# ✅ Tur Serializer (Bütün turları JSON formatında göndərir)
class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'  # Bütün sahələri JSON olaraq göndərir

# ✅ Rezervasiya Serializer (İstifadəçilər üçün)
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')  # 🟢 İstifadəçi email-i göstərilir

    class Meta:
        model = Booking
        fields = ['id', 'user', 'tour', 'num_seats', 'created_at']  # 🔗 Yalnız lazımlı sahələri göndər

    def validate_num_seats(self, value):
        """ 🛑 Boş yer yoxdursa rezervasiya etməyə icazə vermə """
        tour_id = self.initial_data.get("tour")  # POST sorğusundakı turun ID-ni götür
        tour = get_object_or_404(Tour, id=tour_id)  # Tour obyektini bazadan götür

        if tour.available_seats < value:
            raise serializers.ValidationError(f"Yalnız {tour.available_seats} yer mövcuddur.")
        return value

    def create(self, validated_data):
        """ ✅ Rezervasiya yaradıldıqdan sonra turun available_seats sahəsini yenilə """
        tour = validated_data['tour']
        num_seats = validated_data['num_seats']

        if tour.available_seats < num_seats:
            raise serializers.ValidationError(f"Bu tur üçün yalnız {tour.available_seats} yer mövcuddur.")

        # Mövcud yerləri yenilə
        tour.available_seats -= num_seats
        tour.save()

        return super().create(validated_data)
