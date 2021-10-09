# -*- coding: utf-8 -*-

from django import template
from django.forms import TextInput


class AddressWithMapWidget(TextInput):
    width = 700
    height = 200
    zoom = 16

    tpl = "{{% load easy_maps_tags %}}{{% easy_map address {0.width} {0.height} {0.zoom} %}}"

    def render(self, name, value, attrs=None, renderer=None):
        output = super(AddressWithMapWidget, self).render(name, value, attrs, renderer)

        t = template.Template(self.tpl.format(self))
        context = template.Context(
            {
                "address": value,
            }
        )
        return output + t.render(context)
