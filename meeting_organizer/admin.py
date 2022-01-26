from django.contrib import admin

from .models import ProductManager, Student, Meeting


class ProductManagerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'worktime_from',
        'worktime_to',
        'telegram_username'
    ]


class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'worktime_from',
        'worktime_to',
        'telegram_username'
    ]


class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        'time',
        'product_manager',
    ]


admin.site.register(ProductManager, ProductManagerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Meeting, MeetingAdmin)

