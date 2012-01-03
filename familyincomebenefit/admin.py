from django.contrib import admin
from commercialvehicle.models import *


class PolicyInline(admin.StackedInline):
    model = Policy
    extra = 1

class QuoteInline(admin.StackedInline):
    model = Quote
    extra = 1

class RiskAdmin(admin.ModelAdmin):
    inlines = [PolicyInline,QuoteInline]

admin.site.register(Risk, RiskAdmin)

