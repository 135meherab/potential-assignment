from django.db import models

from core.models import BaseModel


class Country(BaseModel):
    country_short = models.CharField(max_length=10)
    country_long = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Countries"


class Province(BaseModel):
    province_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.province_name


class City(BaseModel):
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name="cities"
    )
    city_name = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.city_name}, {self.province.province_name}"


class Language(BaseModel):
    language_name = models.CharField(max_length=255, blank=True)
