import contextlib
import random

from django.conf import settings
from django.contrib.auth.password_validation import (
    validate_password as validate_input_password,
)
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers, validators

from authentications.models import User, UserInformation
from options.models import City, Country, Language, Province
from options.serializers import (
    CitySerializer,
    CountrySerializer,
    LanguageSerializer,
    OnlyProvinceSerializer,
)

from . import UserInformationSerializer
from .helper_functions import update_related_instance


class RegistrationSerializer(serializers.ModelSerializer):
    """
    New User Registration Serializer
    """

    retype_password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        label="Retype Password",
    )

    full_name = serializers.CharField(
        required=True, write_only=True, source="user_information.full_name"
    )
    role = serializers.ChoiceField(
        choices=User.ROLE,
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "retype_password",
            "full_name",
            "role",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        attrs = self.get_initial()

        if attrs.get("password") != attrs.get("retype_password"):
            raise serializers.ValidationError("Password fields didn't match.")

        # You can add additional password validation here
        validate_input_password(
            password=attrs.get("password"),
            user=User(email=attrs.get("email")),
        )

        return value

    @transaction.atomic()
    def create(self, validated_data):
        information_user = validated_data.pop("user_information")
        validated_data.pop("retype_password")
        user = User.objects.create_user(**validated_data, oauth_provider="email")
        update_related_instance(user, information_user, "user_information")
        return user

    @transaction.atomic()
    def update(self, instance, validated_data):
        validated_data.pop("role", None)
        validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        information_user = validated_data.pop("user_information", {})
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save(update_fields=["password"])
        update_related_instance(instance, information_user, "user_information")
        return instance


class AdminUserInformationSerializer(UserInformationSerializer):
    phone_number = serializers.CharField(required=True)

    class Meta(UserInformationSerializer.Meta):
        read_only_fields = (
            "is_phone_verified",
        )  # Remove phone_number from read_only_fields

    def validate_phone_number(self, value):
        if not value:
            return value

        if not value.isdigit():
            raise serializers.ValidationError(_("Phone number must be numeric."))

        queryset = UserInformation.objects.filter(phone_number=value)
        if self.instance and self.instance.user_information:
            queryset = queryset.exclude(id=self.instance.user_information.id)

        if queryset.exists():
            raise validators.ValidationError(_("This phone number is already in use."))

        return value


class AdminUserSerializer(RegistrationSerializer):
    """
    Admin User Registration Serializer
    """

    role = serializers.ChoiceField(choices=User.ROLE, default="admin")
    user_information = AdminUserInformationSerializer()

    class Meta(RegistrationSerializer.Meta):
        fields = [
            "id",
            "role",
            "email",
            "password",
            "retype_password",
            "is_verified",
            "is_active",
            "is_superuser",
            "is_staff",
            "user_information",
        ]
        read_only_fields = ["id", "is_verified", "is_staff", "is_superuser"]

    @transaction.atomic()
    def create(self, validated_data):
        is_active = validated_data.pop("is_active", True)
        user = super().create(validated_data)
        user.is_verified = True
        user.is_active = is_active
        user.save(update_fields=["is_verified", "is_active"])
        return user

    @transaction.atomic()
    def update(self, instance, validated_data):
        is_active = validated_data.pop("is_active", instance.is_active)
        instance = super().update(instance, validated_data)
        instance.is_active = is_active
        instance.save(update_fields=["is_active"])
        return instance
