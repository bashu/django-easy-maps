from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Address
from .widgets import AddressWithMapWidget


class HasExceptionFilter(admin.SimpleListFilter):
    title = _("exception")
    parameter_name = "has_exception"

    def lookups(self, request, model_admin):
        return (
            (1, _("Yes")),
            (0, _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            ids = Address.objects.exclude(exception="").values_list("pk", flat=True)

            if self.value() == "1":
                return queryset.filter(pk__in=ids)

            if self.value() == "0":
                return queryset.exclude(pk__in=ids)

        return queryset


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "address",
        "computed_address",
        "latitude",
        "longitude",
        "has_exception",
    ]
    list_filter = [HasExceptionFilter]
    search_fields = ["address"]

    class Form(forms.ModelForm):
        class Meta:
            widgets = {"address": AddressWithMapWidget({"class": "vTextField"})}

    form = Form
