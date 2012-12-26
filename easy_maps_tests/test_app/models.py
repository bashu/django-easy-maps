#hello, testrunner!
from django.db import models
from django.contrib import admin

from easy_maps.models import Address
from easy_maps.admin import AddressInlineAdmin

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def count(self):
        return self.shop_set.count()

class Shop(Address):
    brand = models.ForeignKey(Brand)

class ShopInlineAdmin(AddressInlineAdmin):
    model = Shop

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'count',]
    model = Brand
    inlines = [
        ShopInlineAdmin,
    ]

admin.site.register(Brand, BrandAdmin)
