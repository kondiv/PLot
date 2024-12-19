from django.shortcuts import render, redirect
from django.http import JsonResponse
from parking.models import Parking, MetroStations, ColorsOfStations, ParkingMetroStations, Floor, ParkingLot
from django.contrib import messages
from .utils import calculate_parking_price



def home(request):
    return render(request, "MainPage.html")

def all_parking_map(request):
    return render(request, "parking/AllParkingMap.html")

def booking_confirmation(request):
    address = request.GET.get("address", "Не указан")
    free_spaces = request.GET.get("free_spaces", "Неизвестно")
    status = request.GET.get("status", "Неизвестно")
    parking_id = request.GET.get("parking_id")

    floor = Floor.objects.filter(parking_id=parking_id).first()
    base_price = floor.actual_price.amount

    price_now = calculate_parking_price(base_price, is_future_booking=False)

    price_later = calculate_parking_price(base_price, is_future_booking=True)

    context = {
        "address": address,
        "free_spaces": int(free_spaces),
        "status": status,
        "price_now": price_now,
        "price_later": price_later,
        "parking_id": parking_id
    }
    return render(request, "parking/BookingConfirmation.html", context)

def metro_search(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse({"results": []})

    stations = MetroStations.objects.filter(name_of_station__icontains=query)
    results = []

    for station in stations:
        for color in station.colors.all():
            results.append({
                "station_id": station.id,
                "station_name": station.name_of_station,
                "color_id": color.id,
                "color": color.color,
            })

    return JsonResponse({"results": results})

def add_parking(request):
    if request.method == "POST":
        address = request.POST.get("address")
        metro_station_ids = request.POST.getlist("metro_station[]")
        metro_color_ids = request.POST.getlist("metro_color[]")
        numbers_of_floors = request.POST.get("numbers_of_floors")
        uploaded_file = request.FILES.get("uploaded_file")
        price = request.POST.get("price")

        if not address or not metro_station_ids or not metro_color_ids:
            messages.error(request, "Пожалуйста, заполните все поля.")
            return redirect("add_parking")

        parking = Parking.objects.create(
            user_id=request.user,
            address=address,
            states=Parking.WAITSAPROVED,
            numbers_of_floors=numbers_of_floors,
        )

        for station_id in metro_station_ids:
            ParkingMetroStations.objects.create(
                station_id=station_id,
                parking=parking,
            )

        for level in range(1, int(numbers_of_floors) + 1):
            floor = Floor.objects.create(
                parking_id=parking,
                parking_lots=10,
                level=level,
                actual_price=price,
            )

            ParkingLot.objects.bulk_create([
                ParkingLot(floor_id=floor, parking_id=parking) for _ in range(10)
            ])

        if uploaded_file:
            request.user.uploaded_file = uploaded_file
            request.user.save()

        messages.success(request, "Парковка успешно создана. Ожидайте подтверждения верификации.")
        return redirect("users:owner_profile")

    metro_stations = MetroStations.objects.all()
    metro_colors = ColorsOfStations.objects.all()

    return render(request, "user/owner/Add_Parking.html", {
        "metro_stations": metro_stations,
        "metro_colors": metro_colors,
    })


def search_parking_by_metro(request):
    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse({"results": []})

    matched_stations = MetroStations.objects.filter(name_of_station__icontains=query)
    parking_results = []

    parking_ids = set(
        ParkingMetroStations.objects.filter(station__in=matched_stations)
        .values_list("parking_id", flat=True)
    )
    parkings = Parking.objects.filter(id__in=parking_ids, states=Parking.ACTIVE)

    for parking in parkings:
        parking_and_stations = ParkingMetroStations.objects.filter(parking=parking).select_related("station")

        station_dict = {}
        for parking_station in parking_and_stations:
            station_name = parking_station.station.name_of_station
            colors = [color.color for color in parking_station.station.colors.all()]

            if station_name in station_dict:
                station_dict[station_name].extend(colors)
            else:
                station_dict[station_name] = colors

        station_info = [
            {"name": station, "colors": list(set(colors))}
            for station, colors in station_dict.items()
        ]

        total_lots = parking.get_total_parking_lots() + parking.get_occupied_parking_lots()
        occupied_percentage = (
            round((parking.get_occupied_parking_lots() / total_lots) * 100, 2)
            if total_lots > 0
            else 0
        )

        parking_results.append({
            "id": parking.id,
            "address": parking.address,
            "stations": station_info,
            "free_spaces": parking.get_total_parking_lots(),
            "load_percentage": occupied_percentage,
        })

    return JsonResponse({"results": parking_results})

