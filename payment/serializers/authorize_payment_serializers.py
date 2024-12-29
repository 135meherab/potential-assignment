import contextlib

from django.conf import settings
from rest_framework import generics, serializers

# from order_management.models import Order
from utils.modules.payment import AuthorizeNet


class MakePaymentSerializers(serializers.Serializer):
    order_id = serializers.IntegerField()
    use_saved_card = serializers.BooleanField(default=False)
    # If card is not saved
    card_number = serializers.CharField(max_length=16, required=False)
    card_expiry = serializers.CharField(max_length=7, required=False)
    card_cvv = serializers.CharField(max_length=3, required=False)
    is_save_card = serializers.BooleanField(default=False)
    # If card is saved
    customer_payment_profile_id = serializers.CharField(max_length=255, required=False)
    # Billing Address
    billing_first_name = serializers.CharField(max_length=50, required=False)
    billing_last_name = serializers.CharField(max_length=50, required=False)
    billing_company = serializers.CharField(max_length=50, required=False)
    billing_address = serializers.CharField(max_length=255, required=False)
    billing_city = serializers.CharField(max_length=50, required=False)
    billing_state = serializers.CharField(max_length=50, required=False)
    billing_zipcode = serializers.CharField(max_length=10, required=False)
    billing_country = serializers.CharField(max_length=50, required=False)

    def __init__(self, instance=None, *args, **kwargs):
        self.order = None
        super().__init__(instance, *args, **kwargs)

    def get_fields(self):
        fields = super().get_fields()

        with contextlib.suppress(AttributeError):
            # Access the `use_saved_card` value from initial data or context
            use_saved_card = self.initial_data.get("use_saved_card", False)

            if use_saved_card:
                # If using a saved card, make `customer_payment_profile_id` required
                fields["customer_payment_profile_id"].required = True
            else:
                # If not using a saved card, make card fields required
                fields["card_number"].required = True
                fields["card_expiry"].required = True
                fields["card_cvv"].required = True
                fields["billing_first_name"].required = True
                fields["billing_last_name"].required = True
                fields["billing_company"].required = True
                fields["billing_address"].required = True
                fields["billing_city"].required = True
                fields["billing_state"].required = True
                fields["billing_zipcode"].required = True
                fields["billing_country"].required = True

        return fields

    def validate_order_id(self, value):
        request = self.context.get("request")
        # self.order = generics.get_object_or_404(Order, id=value, user=request.user)
        if self.order.payment_status:
            raise serializers.ValidationError("Order is already paid")
        return value

    def create(self, validated_data):
        # self.order.payment_status = True
        # self.order.save()
        authorize_net = AuthorizeNet(
            api_login_id=settings.AUTHORIZE_NET_API_LOGIN_ID,
            transaction_key=settings.AUTHORIZE_NET_TRANSACTION_KEY,
        )
        use_saved_card = self.initial_data.get("use_saved_card", False)
        if use_saved_card:
            payment_status = authorize_net.charge_customer_profile(
                user=self.order.user,
                customer_payment_profile_id=validated_data.get(
                    "customer_payment_profile_id"
                ),
                amount=self.order.total_price,
            )
        else:
            payment_status = authorize_net.charge_credit_card(
                card_number=validated_data.get("card_number"),
                card_expiry=validated_data.get("card_expiry"),
                card_cvc=validated_data.get("card_cvv"),
                amount=self.order.total_price,
                first_name=validated_data.get("billing_first_name"),
                last_name=validated_data.get("billing_last_name"),
                company=validated_data.get("billing_company"),
                address=validated_data.get("billing_address"),
                city=validated_data.get("billing_city"),
                state=validated_data.get("billing_state"),
                zipcode=validated_data.get("billing_zipcode"),
                country=validated_data.get("billing_country"),
                user=self.order.user,
                is_save_card=validated_data.get("is_save_card"),
            )
        return payment_status

    def to_representation(self, instance):
        return instance
