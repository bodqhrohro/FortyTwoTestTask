from django.db import models


def _model_to_tuple(model):
    return (
        model.title,
        model.value,
    )


class GeneralInfo(models.Model):
    title = models.CharField(max_length=256)
    value = models.CharField(max_length=65536)


class Contact(models.Model):
    title = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
