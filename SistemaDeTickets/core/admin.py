from django.contrib import admin

from .models import *


admin.site.register(Stops)
admin.site.register(Transport)
admin.site.register(Bus)
admin.site.register(Train)
admin.site.register(SeatCategory)
admin.site.register(Seat)
admin.site.register(Meal)
admin.site.register(Merchandise)
admin.site.register(Journey)
admin.site.register(JourneyStage)
admin.site.register(JourneySchedule)
admin.site.register(Passenger)
admin.site.register(DetailFoodOrder)
admin.site.register(DetailsMerchandiseOrder)
admin.site.register(PurchaseReceipt)
admin.site.register(Payments)


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["price"]


class TicketSalesAdmin(admin.ModelAdmin):
    readonly_fields = ["price", "purchase_date"]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketSales, TicketSalesAdmin)
