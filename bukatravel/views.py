from django.shortcuts import render

# Create your views here.
# bukatravel/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from bukatravel.api import serilaizers
from rest_framework.decorators import api_view
from django.core.cache import cache


BASE_URL = 'https://apiinternal.orbisway.com'
        
def get_bukatravel_signature():
    data = {
        "user": settings.BUKATRAVEL_USER,
        "password": settings.BUKATRAVEL_PASSWORD,
        "api_key": settings.BUKATRAVEL_API_KEY,
    }

    headers = {
        "Action": "signin",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(f"{BASE_URL}/session/", headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        signature = response_data.get("result", {}).get("response", {}).get("signature")

        if signature:
            cache.set("bukatravel_signature", signature, timeout=3600)
        return signature
    except requests.exceptions.RequestException as e:
        print("Gagal mendapatkan signature:", e)
        return None

# Dapat Signature
def get_signature():
    signature = cache.get("bukatravel_signature")
    if not signature:
        signature = get_bukatravel_signature()
    return signature

# no repeat get orbis api
def call_orbis_api(endpoint, action, payload=None):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'action': action,
        'signature': get_signature()
    }
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json=payload or {}, headers=headers)
    return response

@api_view(['POST'])
def get_balance(request):
    response = call_orbis_api("account", "get_balance")
    return Response(response.json())

@api_view(['POST'])
def search(request):
    serializer = serilaizers.SearchFlightSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("booking/airline", "search", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_destination_list(request):
    serializer = serilaizers.GetDestinationListSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("content", "get_destination_list", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_carriers(request):
    serializer = serilaizers.GetCarriersSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("content", "get_carriers", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_carrier_providers(request):
    serializer = serilaizers.GetCarrierProvidersSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("content", "get_carrier_providers", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def signout(request):
    response = call_orbis_api("session", "signout")
    # hapus redis signature
    cache.delete("bukatravel_signature")
    return Response(response.json())

# helper generic for "booking/airline"
def make_api_view(endpoint, action, serializer_class):
    @api_view(['POST'])
    def view(request):
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            response = call_orbis_api(endpoint, action, serializer.validated_data)
            return Response(response.json())
        return Response(serializer.errors, status=400)
    return view

get_fare_rules = make_api_view("booking/airline", "get_fare_rules", serilaizers.GetFareRulesSerializer)
get_ff_availability = make_api_view("booking/airline", "get_ff_availability", serilaizers.GetFFAvailabilitySerializer)
get_post_seat_availability = make_api_view("booking/airline", "get_post_seat_availability", serilaizers.GetPostSeatAvailabilitySerializer)
get_post_ssr_availability = make_api_view("booking/airline", "get_post_ssr_availability", serilaizers.GetPostSSRAvailabilitySerializer)
get_price_itinerary = make_api_view("booking/airline", "get_price_itinerary", serilaizers.GetPriceItinerarySerializer)
get_printout_list = make_api_view("printout", "get_printout_list", serilaizers.GetPrintoutListSerializer)
get_refund_booking = make_api_view("booking/airline", "get_refund_booking", serilaizers.GetRefundBookingSerializer)
get_reschedule_availability = make_api_view("booking/airline", "get_reschedule_availability", serilaizers.GetRescheduleAvailabilitySerializer)
get_seat_availability = make_api_view("booking/airline", "get_seat_availability", serilaizers.GetSeatAvailabilitySerializer)
get_ssr_availability = make_api_view("booking/airline", "get_ssr_availability", serilaizers.GetSSRAvailabilitySerializer)
issued = make_api_view("booking/airline", "issued", serilaizers.IssuedSerializer)
pre_refund_login_list = make_api_view("booking/airline", "pre_refund_login_list", serilaizers.PreRefundLoginListSerializer)
sell_journeys = make_api_view("booking/airline", "sell_journeys", serilaizers.SellJourneysSerializer)
sell_post_ssrs = make_api_view("booking/airline", "sell_post_ssrs", serilaizers.SellPostSSRSerializer)
sell_reschedule = make_api_view("booking/airline", "sell_reschedule", serilaizers.SellRescheduleSerializer)
sell_ssrs = make_api_view("booking/airline", "sell_ssrs", serilaizers.SellSSRsSerializer)
update_booking = make_api_view("booking/airline", "update_booking", serilaizers.UpdateBookingSerializer)
update_contacts = make_api_view("booking/airline", "update_contacts", serilaizers.UpdateContactsSerializer)
update_passengers = make_api_view("booking/airline", "update_passengers", serilaizers.UpdatePassengersSerializer)
assign_seats = make_api_view("booking/airline", "assign_seats", serilaizers.AssignSeatsSerializer)
assign_post_seats = make_api_view("booking/airline", "assign_post_seats", serilaizers.AssignPostSeatsSerializer)
commit_booking = make_api_view("booking/airline", "commit_booking", serilaizers.CommitBookingSerializer)
cancel = make_api_view("booking/airline", "cancel", serilaizers.CancelBookingSerializer)
get_booking = make_api_view("booking/airline", "get_booking", serilaizers.GetBookingSerializer)
