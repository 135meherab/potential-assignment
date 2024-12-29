from django.db import models


def update_related_instance(instance, data, related_attr):
    related_instance = getattr(instance, related_attr)
    attributes = []
    for attr, value in data.items():
        if hasattr(related_instance, attr):
            field = related_instance._meta.get_field(attr)
            if isinstance(field, models.ManyToManyField):
                getattr(related_instance, attr).set(value)
            elif field.concrete:
                setattr(related_instance, attr, value)
                attributes.append(attr)
    related_instance.save(update_fields=attributes)
