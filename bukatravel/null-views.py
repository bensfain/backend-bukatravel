from django.shortcuts import render

# Create your views here.
# bukatravel/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings
from bukatravel.api import serializers
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
        
        #Ambil result
        result = response_data.get('result', {})
        
        #  Cek Error Code Dulu
        error_code = result.get("error_code")
        
        # Jika error_code BUKAN 0, berarti Gagal Login
        if error_code != 0:
            print("\n" + "!"*30)
            print(f"❌ GAGAL LOGIN KE ORBIS!")
            print(f"Error Code: {error_code}")
            print(f"Pesan: {result.get('error_msg')}")
            print("!"*30 + "\n")
            return None
        
        
        # Jika Lolos (Login Sukses), baru ambil signature
        response_obj = result.get("response")
        
        signature = None        
        
        #signature = response_data.get("result", {}).get("response", {}).get("signature")
        #cek bentuk result apakah berbentuk dictionary
        if isinstance(response_obj, dict):
            # Kalau Dictionary, lanjut ambil signature
            signature = response_obj.get("signature")

        if signature:
            cache.set("bukatravel_signature", signature, timeout=3600)
        return signature
    
    except requests.exceptions.RequestException as e:
        print("Gagal Koneksi ke orbis:", e)
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
    serializer = serializers.SearchFlightSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("booking/airline", "search", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_destination_list(request):
    serializer = serializers.GetDestinationListSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("content", "get_destination_list", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_carriers(request):
    serializer = serializers.GetCarriersSerializer(data=request.data)
    if serializer.is_valid():
        response = call_orbis_api("content", "get_carriers", serializer.validated_data)
        return Response(response.json())
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_carrier_providers(request):
    serializer = serializers.GetCarrierProvidersSerializer(data=request.data)
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

get_fare_rules = make_api_view("booking/airline", "get_fare_rules", serializers.GetFareRulesSerializer)
get_ff_availability = make_api_view("booking/airline", "get_ff_availability", serializers.GetFFAvailabilitySerializer)
get_post_seat_availability = make_api_view("booking/airline", "get_post_seat_availability", serializers.GetPostSeatAvailabilitySerializer)
get_post_ssr_availability = make_api_view("booking/airline", "get_post_ssr_availability", serializers.GetPostSSRAvailabilitySerializer)
get_price_itinerary = make_api_view("booking/airline", "get_price_itinerary", serializers.GetPriceItinerarySerializer)
get_printout_list = make_api_view("printout", "get_printout_list", serializers.GetPrintoutListSerializer)
get_refund_booking = make_api_view("booking/airline", "get_refund_booking", serializers.GetRefundBookingSerializer)
get_reschedule_availability = make_api_view("booking/airline", "get_reschedule_availability", serializers.GetRescheduleAvailabilitySerializer)
get_seat_availability = make_api_view("booking/airline", "get_seat_availability", serializers.GetSeatAvailabilitySerializer)
get_ssr_availability = make_api_view("booking/airline", "get_ssr_availability", serializers.GetSSRAvailabilitySerializer)
issued = make_api_view("booking/airline", "issued", serializers.IssuedSerializer)
pre_refund_login_list = make_api_view("booking/airline", "pre_refund_login_list", serializers.PreRefundLoginListSerializer)
sell_journeys = make_api_view("booking/airline", "sell_journeys", serializers.SellJourneysSerializer)
sell_post_ssrs = make_api_view("booking/airline", "sell_post_ssrs", serializers.SellPostSSRSerializer)
sell_reschedule = make_api_view("booking/airline", "sell_reschedule", serializers.SellRescheduleSerializer)
sell_ssrs = make_api_view("booking/airline", "sell_ssrs", serializers.SellSSRsSerializer)
update_booking = make_api_view("booking/airline", "update_booking", serializers.UpdateBookingSerializer)
update_contacts = make_api_view("booking/airline", "update_contacts", serializers.UpdateContactsSerializer)
update_passengers = make_api_view("booking/airline", "update_passengers", serializers.UpdatePassengersSerializer)
assign_seats = make_api_view("booking/airline", "assign_seats", serializers.AssignSeatsSerializer)
assign_post_seats = make_api_view("booking/airline", "assign_post_seats", serializers.AssignPostSeatsSerializer)
commit_booking = make_api_view("booking/airline", "commit_booking", serializers.CommitBookingSerializer)
cancel = make_api_view("booking/airline", "cancel", serializers.CancelBookingSerializer)
get_booking = make_api_view("booking/airline", "get_booking", serializers.GetBookingSerializer)
