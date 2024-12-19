from django.db import models
from parking.models import ParkingLot
from djmoney.models.fields import MoneyField
from user.models import User

class Booking(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец брони',
    )

    parking_lot_id = models.ForeignKey(
        ParkingLot,
        on_delete=models.CASCADE,
        verbose_name='ID парковочного места',
    )

    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='RUB',
        max_digits=20,
        verbose_name="Цена"
    )

    def __str__(self):
        return self.user_id.username + " " + self.parking_lot_id.parking_id.address + " ID места: " + str(self.parking_lot_id.id)