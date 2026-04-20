# bukatravel/serializers.py
from rest_framework import serializers


class BukatravelSigninSerializer(serializers.Serializer):
    user = serializers.CharField()
    password = serializers.CharField()
    api_key = serializers.CharField()

class JourneyListSerializer(serializers.Serializer):
    origin = serializers.CharField()
    destination = serializers.CharField()
    departure_date = serializers.DateField()

class SearchFlightSerializer(serializers.Serializer):
    journey_list = JourneyListSerializer(many=True)
    adult = serializers.IntegerField()
    child = serializers.IntegerField()
    infant = serializers.IntegerField()
    cabin_class = serializers.CharField()
    carrier_codes = serializers.ListField(child=serializers.CharField(), required=False)
    is_combo_price = serializers.BooleanField()
    provider = serializers.CharField()
    promo_codes = serializers.ListField(child=serializers.CharField(), required=False)


class GetDestinationListSerializer(serializers.Serializer):
    provider_type = serializers.CharField()


class GetCarriersSerializer(serializers.Serializer):
    provider_type = serializers.CharField()


class GetCarrierProvidersSerializer(serializers.Serializer):
    provider_type = serializers.CharField()


class GetFareRulesSerializer(serializers.Serializer):
    journey_code = serializers.CharField()
    fare_code = serializers.CharField()
    provider = serializers.CharField()


class GetFFAvailabilitySerializer(serializers.Serializer):
    provider = serializers.CharField()
    ff_numbers = serializers.ListField(child=serializers.CharField())


class GetPostSeatAvailabilitySerializer(serializers.Serializer):
    order_number = serializers.CharField()


class GetPostSSRAvailabilitySerializer(serializers.Serializer):
    order_number = serializers.CharField()


class GetPriceItinerarySerializer(serializers.Serializer):
    journey_ref_id = serializers.CharField()
    fare_ref_ids = serializers.ListField(child=serializers.CharField())
    provider = serializers.CharField()


class GetPrintoutListSerializer(serializers.Serializer):
    order_number = serializers.CharField()


class GetRefundBookingSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    captcha_code = serializers.CharField()


class GetRescheduleAvailabilitySerializer(serializers.Serializer):
    order_number = serializers.CharField()
    provider = serializers.CharField()


class GetSeatAvailabilitySerializer(serializers.Serializer):
    order_number = serializers.CharField()


class GetSSRAvailabilitySerializer(serializers.Serializer):
    order_number = serializers.CharField()


class IssuedSerializer(serializers.Serializer):
    order_number = serializers.CharField()


class PreRefundLoginListSerializer(serializers.Serializer):
    order_number = serializers.CharField()


class SellJourneysSerializer(serializers.Serializer):
    journey_code = serializers.CharField()
    fare_code = serializers.CharField()
    provider = serializers.CharField()


class SellPostSSRSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    ssr_requests = serializers.ListField(child=serializers.DictField())


class SellRescheduleSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    schedule_code = serializers.CharField()
    provider = serializers.CharField()


class SellSSRsSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    ssr_requests = serializers.ListField(child=serializers.DictField())


class UpdateBookingSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    remarks = serializers.CharField(required=False)


class UpdateContactsSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    contacts = serializers.ListField(child=serializers.DictField())


class UpdatePassengersSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    passengers = serializers.ListField(child=serializers.DictField())


class AssignSeatsSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    segment_seat_request = serializers.ListField(child=serializers.DictField())


class AssignPostSeatsSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    segment_seat_request = serializers.ListField(child=serializers.DictField())

class CommitBookingSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    force_issued = serializers.BooleanField(default=False)

class CancelBookingSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    cancel_type = serializers.ChoiceField(choices=["void", "refund"])

class GetBookingSerializer(serializers.Serializer):
    order_number = serializers.CharField()
