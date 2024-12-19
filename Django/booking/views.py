from parking.models import Parking
from .models import ParkingLot, Booking
from django.shortcuts import render, redirect, get_object_or_404


def payment(request):
    parking_id = request.GET.get('parking_id')
    price = request.GET.get('price')

    parking = get_object_or_404(Parking, id=parking_id)

    if parking.get_total_parking_lots() > 0:
        free_parking_lot = ParkingLot.objects.filter(parking_id=parking, is_free=True).first()

        if free_parking_lot:
            free_parking_lot.is_free = False
            free_parking_lot.save()

            Booking.objects.create(
                user_id=request.user,
                parking_lot_id=free_parking_lot,
                price=price,
            )

            return render(request, "parking/Payment.html")

    return render(request, "parking/Payment.html")


