# -*- coding: utf-8 -*-

from django.db import models


#### California Taxes -
# Many of these are not used, as the taxes are currently hardcoded - which is faster anyway.
# at some point, perhaps, this should be redone into 1 (or some minimim) table(s) with fixtures,
# and loaded into a dict at module-load time.
'''
class Cacounties(models.Model):
    city = models.CharField(max_length=50)
    tax = models.FloatField()
    county = models.CharField(max_length=20)
    class Meta:
        db_table = u'cacounties'

class Cacountytax(models.Model):
    city = models.CharField(max_length=50)
    tax = models.FloatField()
    county = models.CharField(max_length=20)
    class Meta:
        db_table = u'cacountytax'

class Cacountycounts(models.Model):
    county = models.CharField(max_length=20)
    tax = models.FloatField()
    count = models.IntegerField()
    class Meta:
        db_table = u'cacountycounts'

class Cacountytaxcounts(models.Model):
    county = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    tax = models.FloatField()
    count = models.IntegerField()
    class Meta:
        db_table = u'cacountytaxcounts'
'''

class Catax(models.Model):
    name    = models.CharField(max_length=150, unique=True, help_text='County, plus city in parens for rate exceptions')
    county  = models.CharField(max_length=50, help_text="County name only")
    tax     = models.DecimalField (max_digits=5, decimal_places=2, help_text='Total CA Sales Tax rate')
    #city   = models.CharField(max_length=50)
    cities  = models.CommaSeparatedIntegerField (max_length=3000, blank=True, help_text='Comma-separated list of cities within the county for which this tax rate applies')
    count   = models.IntegerField(help_text='Count of cities, used to determine the need for the city to be added to the county for uniqueness')

    created     = models.DateTimeField (auto_now_add=True)
    updated     = models.DateTimeField (auto_now=True)

    def __unicode__ (self):
        return self.name

    class Meta:
        db_table = u'catax'
        unique_together = ('county','tax')
        verbose_name = 'CA Tax'
        verbose_name_plural = 'CA Taxes'
        ordering=('name',)


#### Set up single-seq tables (org fm legacy eracks db - all db id's in one sequence)

#from apps
import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=Catax)

