from django.urls import path

from apps.contact_page import views as contact_page_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('', contact_page_views.contact_page, name='index'),
    path('admin/', admin.site.urls),
]
