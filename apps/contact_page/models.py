from django.db import models


def _model_to_tuple(model):
    return (
        model.title,
        model.value,
    )


def _keyvalue_to_str(key, value):
    return (key + ': ' if key else '') + value


class GeneralInfo(models.Model):
    title = models.CharField(max_length=256)
    value = models.CharField(max_length=65536)

    def __str__(self):
        return _keyvalue_to_str(self.title, self.value)


class Contact(models.Model):
    title = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    def __str__(self):
        return _keyvalue_to_str(self.title, self.value)
