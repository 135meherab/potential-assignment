import contextlib

from django.db import transaction
from django.db.models import Avg
from rest_framework import serializers

from authentications.models import User, UserInformation, UserTwoStepVerification
from options.models import City, Country, Language, Province
from options.serializers import (
    CitySerializer,
    CountrySerializer,
    LanguageSerializer,
    OnlyProvinceSerializer,
)

from .helper_functions import update_related_instance


class BasicUserInformationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user_information.full_name")
    profile_picture = serializers.ImageField(source="user_information.profile_picture")

    class Meta:
        model = User
        fields = (
            "full_name",
            "profile_picture",
        )


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = (
            "full_name",
            "profile_picture",
            "gender",
            "date_of_birth",
            "language",
            "country",
            "province",
            "city",
            "address",
            "phone_number",
            "is_phone_verified",
        )
        read_only_fields = (
            # 'phone_number',
            "is_phone_verified",
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["language"] = LanguageSerializer(instance.language).data
        response["country"] = CountrySerializer(instance.country).data
        response["province"] = OnlyProvinceSerializer(instance.province).data
        response["city"] = CitySerializer(instance.city).data
        return response


class BaseUserSerializer(serializers.ModelSerializer):
    user_information = UserInformationSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "user_information",
            "oauth_provider",
            "date_joined",
            "is_active",
            "is_staff",
            "role",
        )
        read_only_fields = (
            "id",
            "email",
            "oauth_provider",
            "date_joined",
            "is_active",
            "is_staff",
            "role",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        if user_information := validated_data.pop("user_information", None):
            # Update the UserInformation fields or related object
            update_related_instance(instance, user_information, "user_information")

        return instance


class PersonalProfileSerializer(BaseUserSerializer):

    # nanny_information = NannyInformationSerializer(required=False)

    class Meta(BaseUserSerializer.Meta):
        fields = (
            BaseUserSerializer.Meta.fields
            # + ('nanny_information',)
        )

    def get_fields(self):
        """
        Conditionally include nanny information based on user role
        """
        fields = super().get_fields()
        # request = self.context.get('request')
        #
        # # if not (request and request.user.is_authenticated and request.user.role == 'nanny'):
        # #     fields.pop('nanny_information', None)

        return fields

    @transaction.atomic
    def update(self, instance, validated_data):
        # if nanny_information := validated_data.pop("nanny_information", None):
        #     update_related_instance(instance, nanny_information, "nanny_information")

        return super().update(instance, validated_data)


class SendInvitationSerializer(serializers.Serializer):
    email = serializers.ListField(child=serializers.EmailField())
