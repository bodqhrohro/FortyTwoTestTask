from django.contrib import admin
from django import forms

from .models import GeneralInfo, Contact


class GeneralInfoAdminForm(forms.ModelForm):
    title = forms.CharField()
    value = forms.CharField(widget=forms.Textarea)


class GeneralInfoAdmin(admin.ModelAdmin):
    form = GeneralInfoAdminForm


admin.site.register(GeneralInfo, GeneralInfoAdmin)
admin.site.register(Contact)
