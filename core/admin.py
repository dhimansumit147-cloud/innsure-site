from django.contrib import admin
from .models import Contact, Service, Hospital, Slider


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('heading', 'name', 'created_at')
    search_fields = ('heading', 'name')
    list_filter = ('created_at',)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    search_fields = ('title',)
    list_filter = ('status', 'created_at')