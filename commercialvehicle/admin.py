from django.contrib import admin
from commercialvehicle.models import *


class PolicyInline(admin.StackedInline):
    model = Policy
    extra = 1

class QuoteInline(admin.StackedInline):
    model = Quote
    extra = 1

class ClaimInline(admin.StackedInline):
    model = Claim
    extra = 1

class ConvictionInline(admin.StackedInline):
    model = Conviction
    extra = 1
    
class VehicleAddressInline(admin.StackedInline):
    model = VehicleAddress

class RiskAdmin(admin.ModelAdmin):
    inlines = [PolicyInline,QuoteInline]

class CommercialDriverAdmin(admin.ModelAdmin):
    inlines = [ClaimInline,ConvictionInline]

class VehicleAdmin(admin.ModelAdmin):
    inlines = [VehicleAddressInline]

admin.site.register(Risk, RiskAdmin)
admin.site.register(CommercialDriver, CommercialDriverAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(ClusterProfile)
#admin.site.register(Policy)
#admin.site.register(Quote)
#admin.site.register(Address)
#admin.site.register(Claim)
#admin.site.register(Conviction)


