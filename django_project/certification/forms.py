# coding=utf-8
from __future__ import unicode_literals
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Submit,
    Field,
)
from models import (
    CertifyingOrganisation,
)
from django.contrib.gis.forms.widgets import BaseGeometryWidget
from django.contrib.gis import gdal


class CertifyingOrganisationForm(forms.ModelForm):

    # noinspection PyClassicStyleClass
    class Meta:
        model = CertifyingOrganisation
        fields = (
            'name',
            'organisation_email',
            'address',
            'country',
            'organisation_phone',
            'organisation_owners'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.project = kwargs.pop('project')
        form_title = 'New Certifying Organisation for %s' % self.project.name
        self.helper = FormHelper()
        layout = Layout(
            Fieldset(
                form_title,
                Field('name', css_class='form-control'),
                Field('organisation_email', css_class='form-control'),
                Field('address', css_class='form-control'),
                Field('country', css_class='form-control chosen-select'),
                Field('organisation_phone', css_class='form-control'),
                Field('organisation_owners',
                      widget=forms.CheckboxSelectMultiple,
                      choices=self.user),
                css_id='project-form')
        )
        self.helper.layout = layout
        self.helper.html5_required = False
        super(CertifyingOrganisationForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        instance = super(CertifyingOrganisationForm, self).save(commit=False)
        instance.project = self.project
        instance.approved = False
        instance.save()
        self.save_m2m()
        return instance


class CustomOSMWidget(BaseGeometryWidget):
    """An OpenLayers/OpenStreetMap-based widget."""
    template_name = 'gis/openlayers-osm.html'
    default_lon = 20
    default_lat = -29

    class Media:
        js = (
            '/static/js/libs/OpenLayers-2.13.1/OpenLayers.js',
            '/static/js/libs/OpenLayers-2.13.1/OpenStreetMapSSL.js',
            '/static/js/libs/OLMapWidget.js'
        )

    def __init__(self, attrs=None):
        super(CustomOSMWidget, self).__init__()
        for key in ('default_lon', 'default_lat'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)

    @property
    def map_srid(self):
        # Use the official spherical mercator projection SRID when GDAL is
        # available; otherwise, fallback to 900913.
        if gdal.HAS_GDAL:
            return 3857
        else:
            return 900913