from django.contrib import admin
from parking.models import Parking
from parking.models import Floor
from parking.models import ParkingLot
from parking.models import MetroStationsColorsOfStations
from parking.models import MetroStations
from parking.models import ColorsOfStations
from parking.models import ParkingMetroStations

# Register your models here.
admin.site.register(Parking)
admin.site.register(Floor)
admin.site.register(ParkingLot)
admin.site.register(MetroStationsColorsOfStations)
admin.site.register(MetroStations)
admin.site.register(ColorsOfStations)
admin.site.register(ParkingMetroStations)
