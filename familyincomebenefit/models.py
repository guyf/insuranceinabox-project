import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from easymode.tree.xml.decorators import toxml
from easy_maps.models import Address


@toxml
class Risk(models.Model):
    name = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User)
    #FK one clusterprofile 
    #FK many quote
    #FK many policy
    #FK one lifeinsured
    def __unicode__(self):
        return self.name
    
    def __serialize__(self, stream):
        self._rec_serialize(self, stream)
        
    def _rec_serialize(self, obj, stream):
        stream.startElement(obj._meta.object_name, {})
        for field in obj._meta.fields:
            stream.startElement(field.name, {})
            stream.characters(field.value_to_string(obj))
            stream.endElement(field.name)
        for relobj_desc in obj._meta.get_all_related_objects():
            relobj = getattr(obj, relobj_desc.get_accessor_name())
            if hasattr(relobj, 'iterator'):
                for o in relobj.get_query_set():
                    self._rec_serialize(o, stream)
            else:
                stream.startElement(relobj._meta.object_name, {})
                for f in relobj._meta.fields:
                    stream.startElement(f.name, {})
                    stream.characters(f.value_to_string(relobj))
                    stream.endElement(f.name)
                stream.endElement(relobj._meta.object_name)
        stream.endElement(obj._meta.object_name)


class ClusterProfile(models.Model):
    risk = models.OneToOneField(Risk)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=400, blank=True)


class LifeInsured(models.Model):
    risk = models.OneToOneField(Risk)
    user = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    SEXES = (
    ('M', u'Male'),
    ('F', u'Female')
    )
    sex = models.CharField(max_length=1, choices=SEXES)
    dob = models.DateField(verbose_name='Date of birth')
    is_smoker = models.BooleanField(default=False)
    term_years = models.IntegerField(verbose_name='How long do you need cover for')
    annual_amount = models.IntegerField(verbose_name='How much do you need per year')    

    def __unicode__(self):
        return str(self.first_name + ' ' + self.last_name)
        
class Address(models.Model):
    vehicle = models.OneToOneField(Vehicle, null=True)
    geocoded_address = models.ForeignKey(Address, blank=True, null=True)
    flat_number = models.CharField(_('Flat No'), max_length = 20, blank = True)
    number = models.CharField(_('Building Name or Number'), max_length = 20)
    street_line1 = models.CharField(_('Address 1'), max_length = 100)
    street_line2 = models.CharField(_('Address 2'), max_length = 100, blank = True)
    city = models.CharField(_('City'), max_length = 100)
    county = models.CharField(_('County'), max_length = 100, blank = True)
    postcode = models.CharField(_('Postcode'), max_length = 9)
    country = models.CharField(_('Country'), max_length = 100, blank = True)
    
    def __unicode__(self):
        str_list = []
        for f in self._meta.fields:
            if len(f.value_to_string(self)) and f.value_to_string(self) != 'None':
                    str_list.append(str(f.value_to_string(self) + ', '))
        return ''.join(str_list)
        
class Quote(models.Model):
    risk = models.ForeignKey(Risk)
    amount = models.DecimalField(verbose_name='Amount', max_digits=12, decimal_places=2)
    date = models.DateField(verbose_name='Quote date', default=datetime.date.today())
    validto_date = models.DateField(verbose_name='Quote valid until', default=datetime.date.today())

    def __unicode__(self):
        return self.amount

class Policy(models.Model):
    risk = models.ForeignKey(Risk)
    renewal_date = models.DateField(verbose_name='Renewal Date', default=datetime.date.today())
    number = models.CharField(max_length=30, verbose_name='Policy Number')
    is_onrisk = models.BooleanField(default=False)

    def __unicode__(self):
        return self.number