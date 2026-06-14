from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'book',
        'created_at',
        'plated_end_at',
        'end_at'
    )

    search_fields = (
        'id',
        'user__email',
        'book__name'
    )

    list_filter = (
        'created_at',
        'plated_end_at',
        'end_at'
    )

    readonly_fields = (
        'created_at',
    )