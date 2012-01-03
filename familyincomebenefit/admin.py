from django.contrib import admin
from familyincomebenefit.models import *


class PolicyInline(admin.StackedInline):
    model = Policy
    extra = 1

class QuoteInline(admin.StackedInline):
    model = Quote
    extra = 1
    
class LifeInsuredInline(admin.StackedInline):
    model = LifeInsured
    extra = 1

class FIBRiskAdmin(admin.ModelAdmin):
    inlines = [LifeInsuredInline,PolicyInline,QuoteInline]

admin.site.register(FIBRisk, FIBRiskAdmin)

