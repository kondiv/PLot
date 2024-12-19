from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render, redirect

from booking.models import Booking
from parking.models import Parking, ParkingMetroStations, Floor, ParkingLot, MetroStations
from .forms import DriverRegistrationForm, OwnerRegistrationForm
from django.contrib.auth import authenticate, login, logout


def register(request):
    role = request.GET.get("role", "driver")
    if request.method == "POST":
        form = OwnerRegistrationForm(request.POST, request.FILES) if role == "owner" else DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "parkingowner" if role == "owner" else "driver"
            user.set_password(form.cleaned_data["password"])
            user.save()

            if role == "owner":
                address = request.POST.get("address")
                metro_station= request.POST.get("metro_station[]")
                numbers_of_floors = request.POST.get("numbers_of_floors")
                price = request.POST.get("price")

                parking = Parking.objects.create(
                    user_id=user,
                    address=address,
                    states=Parking.WAITSAPROVED,
                    numbers_of_floors=numbers_of_floors,
                )

                ParkingMetroStations.objects.create(
                    station_id=metro_station,
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

            messages.success(request, "Регистрация прошла успешно!")
            login(request,user)
            return redirect("users:owner_profile") if role == 'owner' else redirect("users:driver_profile")
        else:
            messages.error(request, "Исправьте ошибки в форме!")

    else:
        form = OwnerRegistrationForm() if role == "owner" else DriverRegistrationForm()

    return render(request, "user/Registration.html", {"form": form, "role": role})

def forgot_password(request):
    return render(request, "user/Recover.html")

def owner_profile(request):
    return render(request, "user/owner/Personal_Data.html")

def driver_profile(request):
    return render(request, "user/driver/Personal_Data.html")

def finance(request):
    return render(request, "user/owner/Finance.html")
def feed_back(request):
    return render(request, "user/driver/Feed_Back.html")

def parking_history(request):
    bookings = Booking.objects.filter(user_id=request.user)
    return render(request, "user/driver/Parking_History.html",{"bookings":bookings})

def notices(request):
    return render(request, "user/driver/Notices.html")

def promo_codes(request):
    return render(request, "user/driver/Promo_Codes.html")

def support_and_assistance(request):
    return render(request, "user/driver/Support_and_assistance.html")
def parkings_and_docs(request):
    parkings = Parking.objects.filter(user_id=request.user)
    parkings_with_stations = parkings.prefetch_related(
        Prefetch('parking', queryset=MetroStations.objects.all())
    )
    return render(request, "user/owner/Parkings_Docs.html", {'parkings': parkings_with_stations})

def graphics(request):
    return render(request, "user/owner/Graphics.html")

def user_login(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('MainPage')
        else:
            error_message = 'Неверный email или пароль. Попробуйте снова.'

    return render(request, 'user/Login.html', {'form': request.POST, 'error_message': error_message})

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("MainPage")
    return render(request, "user/Logout.html")

