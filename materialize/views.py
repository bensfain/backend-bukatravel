# from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


def admin_menus(user):
    menus = [
        # dict(
        #     title="Dashboard",
        #     icon="fa fa-tachometer-alt",
        #     url=reverse_lazy("dashboard"),
        # ),
        dict(
            title="Frontend",
            icon="fa fa-home",
            url="/",
        ),
        # dict(
        #     title="Auth Group",
        #     icon="fa fa-newspaper",
        #     url=reverse_lazy("admin:auth_group_changelist"),
        # ),
        # dict(
        #     title="Users",
        #     icon="fa fa-newspaper",
        #     url=reverse_lazy("admin:auth_user_changelist"),
        # ),
        dict(
            title="Booking",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_booking_changelist"),
        ),
        dict(
            title="Flight",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_flight_changelist"),
        ),
        dict(
            title="Hotel",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_hotel_changelist"),
        ),
        dict(
            title="Passenger",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_passenger_changelist"),
        ),
        dict(
            title="Payment",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_payment_changelist"),
        ),
        dict(
            title="Profit",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_profit_changelist"),
        ),
        dict(
            title="Role",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_role_changelist"),
        ),
        dict(
            title="Supplier",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_supplier_changelist"),
        ),
        dict(
            title="Supllier Profit",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_supplierprofit_changelist"),
        ),
        dict(
            title="Transaction Rule",
            icon="fa fa-newspaper",
            url=reverse_lazy("admin:core_transactionrule_changelist"),
        ),
        # dict(
        #     title="Users",
        #     icon="fa fa-newspaper",
        #     url=reverse_lazy("admin:core_user_changelist"),
        # ),
    ]

    return menus


@login_required(login_url=reverse_lazy("login"))
def dashboard(request, extra_cotext={}):
    extra_cotext.update({"title": "Dashboard"})
    return render(request, "dashboard.html", extra_cotext)


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Authentication successful, redirect to a protected page
            if user.is_superuser:
                return redirect(reverse_lazy("dashboard"))
            else:
                return redirect("/home/")
        else:
            # Authentication failed, handle the error
            return render(
                request,
                "admin/login.html",
                {"error_message": "Invalid login credentials"},
            )
    else:
        return render(request, "admin/login.html")


def set_timezone(request):
    if request.method == "POST":
        request.session["django_timezone"] = request.POST["timezone"]
        return HttpResponse(status=200)  # Tanggapi dengan status 200 OK
    else:
        return HttpResponse(status=400)
