from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'company',
        'phone',
        'status',
        'created_at'
    )

    list_filter = ('status',)

    search_fields = (
        'name',
        'company',
        'phone'
    )