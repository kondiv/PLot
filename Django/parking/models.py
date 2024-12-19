from django.db import models
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField
from decimal import Decimal

User = get_user_model()
class Parking(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ID владельца',
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Адрес"
    )

    numbers_of_floors = models.IntegerField(
        validators=[MinValueValidator(1, message="Значение должно быть не меньше 1")],
        verbose_name="Кол-во этажей"
    )

    ACTIVE = "active"
    WAITSFORSETTINGS = "waitsforsettings"
    WAITSAPROVED = "waitsaproved"
    NONACTIVE = "nonactive"

    STATES = (
        (ACTIVE, "Активный"),
        (WAITSFORSETTINGS, "Ожидает настройки"),
        (WAITSAPROVED, "Ожидает подтверждения"),
        (NONACTIVE, "Не активный"),
    )

    states = models.CharField(
        max_length=100, verbose_name="Состояние", choices=STATES, default=WAITSAPROVED
    )

    def get_total_parking_lots(self):
        return ParkingLot.objects.filter(parking_id=self, is_free=True).count()

    def get_occupied_parking_lots(self):
        return ParkingLot.objects.filter(parking_id=self, is_free=False).count()


    def __str__(self):
        return self.address + " " + self.states


class Floor(models.Model):
    parking_id = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE,
        verbose_name='ID парковки',
    )

    parking_lots = models.IntegerField(
        validators=[MinValueValidator(0, message="Значение должно быть не меньше 0")],
        verbose_name="Парковочные места"
    )

    level = models.IntegerField(
        validators=[MinValueValidator(1, message="Значение должно быть не меньше 1")],
        verbose_name="Номер этажа"
    )

    actual_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='RUB',
        max_digits=20,
        verbose_name="Цена"
    )

    def __str__(self):
        return f"Парковка: {self.parking_id.address}, Этаж: {self.level}"

class ParkingLot(models.Model):
    floor_id = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        verbose_name='ID этажа',
    )

    parking_id = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE,
        verbose_name='ID парковки',
    )

    is_for_disabled = models.BooleanField(
        default=False,
        verbose_name="Для инвалидов"
    )

    is_free = models.BooleanField(
        default=True,
        verbose_name="Свободно"
    )

    def __str__(self):
        return f"Парковка: {self.parking_id.address}, Этаж ID: {self.floor_id.id}"

class ColorsOfStations(models.Model):
    color = ColorField(
        default="#FF0000",
        unique=True
    )
    color_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Название цвета",
    )
    def __str__(self):
        return self.color_name

class MetroStations(models.Model):
    name_of_station = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="Название станции",
    )
    colors = models.ManyToManyField(
        to=ColorsOfStations,
        through="MetroStationsColorsOfStations",
        related_name="metro_color",
        verbose_name="Цвет станции",
    )
    parkings = models.ManyToManyField(
        to=Parking,
        through="ParkingMetroStations",
        related_name="parking",
        verbose_name="Парковка",
    )
    def __str__(self):
        return self.name_of_station

class MetroStationsColorsOfStations(models.Model):
    station = models.ForeignKey(
        to=MetroStations,
        on_delete=models.CASCADE,
        verbose_name="Станция",
    )

    station_color = models.ForeignKey(
        to=ColorsOfStations,
        on_delete=models.CASCADE,
        verbose_name="Цвет станции",
    )

    def __str__(self):
        return self.station.name_of_station + " " + self.station_color.color_name

class ParkingMetroStations(models.Model):
    station = models.ForeignKey(
        to=MetroStations,
        on_delete=models.CASCADE,
        verbose_name="Станция",
    )

    parking = models.ForeignKey(
        to=Parking,
        on_delete=models.CASCADE,
        verbose_name="Парковка",
    )

    def __str__(self):
        return self.parking.address + " " + self.station.name_of_station
