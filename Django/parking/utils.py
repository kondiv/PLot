from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()
def parking_owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != User.PARKINGOWNER:
            raise PermissionDenied("Только владельцы парковки могут выполнять это действие.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def calculate_parking_price(base_price, is_future_booking):
    TAX_RATE = Decimal("0.15")
    FUTURE_BOOKING_SURCHARGE = Decimal("400")
    final_price = base_price + (int(base_price) * TAX_RATE)

    if is_future_booking:
        final_price += FUTURE_BOOKING_SURCHARGE

    return final_price
