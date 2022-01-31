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
        'telegram_username',
        'time_interval'
    ]
    readonly_fields = ('telegram_chat_id', 'time_interval', )


class MeetingAdmin(admin.ModelAdmin):
    list_display = ['time', 'product_manager']
    readonly_fields = ('level',)


admin.site.register(ProductManager, ProductManagerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Meeting, MeetingAdmin)

