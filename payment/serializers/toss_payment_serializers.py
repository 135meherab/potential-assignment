import datetime

from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext as _

# Relationship with item. It can be a course, product, or any other item
from product.models import Product
from rest_framework import generics, serializers

from authentications.serializers import BasicUserInformationSerializer
from payment.models import Order
from utils.modules.payment import TossPayments


class OrderSerializer(serializers.ModelSerializer):
    user = BasicUserInformationSerializer(read_only=True)
    # Relationship with item. It can be a course, product, or any other item
    product = serializers.SlugRelatedField(
        queryset=Product.objects.filter(
            publish_date__lte=datetime.date.today(),
            application_start_date__lte=datetime.date.today(),
        ),
        slug_field="slug",
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_id",
            "user",
            "product",
            "amount",
            "status",
            "payment_key",
            "payment_type",
            "payment_response",
        ]
        read_only_fields = [
            "id",
            "order_id",
            "amount",
            "status",
            "payment_key",
            "payment_type",
            "payment_response",
        ]

    def create(self, validated_data):
        try:
            product = validated_data.get("product")
            # Discount system as per the project requirement
            is_discounted = product.is_discounted
            discount_type = product.discount_type
            discount_value = product.discount_value

            if is_discounted:
                if discount_type == "percentage":
                    price = product.price - (product.price * discount_value / 100)
                else:
                    price = product.price - discount_value
            else:
                price = product.price
            return super().create({"amount": round(price, 2), **validated_data})

        except DjangoValidationError as e:
            print(e)
            raise serializers.ValidationError(
                {
                    "product": _("You have already purchased this product."),
                }
            ) from e

    def update(self, instance, validated_data):
        # Prevent updating the order
        return instance


class PaymentSerializer(serializers.Serializer):
    payment_key = serializers.CharField()
    payment_type = serializers.CharField()
    order_id = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.order = None
        self.response_code = None
        self.payment_response = None

        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        request = self.context.get("request")

        payment_key = attrs.get("payment_key")
        order_id = attrs.get("order_id")
        self.order = generics.get_object_or_404(
            Order.objects,
            order_id=order_id,
            user=request.user,
            status="PENDING",
        )

        toss_payments = TossPayments(settings.TOSS_SECRET_KEY)
        self.response_code, self.payment_response = toss_payments.authorize_payment(
            amount=int(self.order.amount), order_id=order_id, payment_key=payment_key
        )
        if self.response_code != 200:
            raise serializers.ValidationError(
                {"payment_key": _("Payment failed. Please try again.")}
            )

        return attrs

    def create(self, validated_data):
        self.order.status = "PAYMENT_COMPLETE"
        self.order.payment_key = validated_data.get("payment_key")
        self.order.payment_type = validated_data.get("payment_type")
        self.order.payment_response = self.payment_response
        self.order.save(
            update_fields=["status", "payment_key", "payment_type", "payment_response"]
        )
        return self.order


class CancelPaymentSerializer(serializers.Serializer):
    order_id = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.order = None
        self.response_code = None
        self.payment_response = None

        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        request = self.context.get("request")

        order_id = attrs.get("order_id")
        self.order = generics.get_object_or_404(
            Order.objects,
            order_id=order_id,
            user=request.user,
            status="PAYMENT_COMPLETE",
        )

        toss_payments = TossPayments(settings.TOSS_SECRET_KEY)
        self.response_code, self.payment_response = toss_payments.cancel_payment(
            payment_key=self.order.payment_key, reason="User requested cancellation"
        )

        if self.response_code != 200:
            raise serializers.ValidationError(
                {"order_id": _("Payment cancellation failed. Please try again.")}
            )

        return attrs

    def create(self, validated_data):
        self.order.status = "CANCELLED"
        self.order.payment_response = self.payment_response
        self.order.save(update_fields=["status", "payment_response"])
        return self.order
