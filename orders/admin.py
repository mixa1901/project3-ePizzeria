from django.contrib import admin

from .models import Dinner_platter, Salad, Pasta, Sub_addon, Sub, Topping, Reg_Pizza, Syc_Pizza, Order, Size

# Register your models here.
admin.site.register(Dinner_platter)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(Sub_addon)
admin.site.register(Sub)
admin.site.register(Topping)
admin.site.register(Reg_Pizza)
admin.site.register(Syc_Pizza)
admin.site.register(Size)


def make_completed(modeladmin, request, queryset):
    queryset.update(status='c')
make_completed.short_description = "Mark selected orders as completed"


def make_declined(modeladmin, request, queryset):
    queryset.update(status='d')
make_declined.short_description = "Mark selected orders as declined"

class OrderAdmin(admin.ModelAdmin):
    list_display = [Order.__str__, 'status']
    ordering = ['-id']
    actions = [make_completed, make_declined]

admin.site.register(Order, OrderAdmin)