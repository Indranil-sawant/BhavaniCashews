from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import Category, Product, ProductGallery, ProductReview , CashewGrade


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, instance):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100" style="border-radius: 4px;" />')
        return "No image uploaded yet"
    
    preview.short_description = "Gallery Image Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'image_preview', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_detail_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "No Image"
    image_preview.short_description = "Preview"

    def image_detail_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" max-width="300" style="max-height: 200px; border-radius: 8px;" />')
        return "No Image"
    image_detail_preview.short_description = "Current Image Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail',
        'name', 
        'category',
        'grade',     
        'price', 
        'stock', 
        'is_available'
    )
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 4px; border: 1px solid #c6c7c0;" />', obj.image.url)
        return "No Image"
    thumbnail.short_description = "Thumbnail"

    list_filter = ('category', 'grade', 'is_featured', 'is_available', 'created_at')
    list_editable = ('price', 'stock', 'is_available')
    search_fields = ('name', 'sku', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductGalleryInline]
    readonly_fields = ('image_detail_preview', 'secondary_image_detail_preview')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'sku', 'price', 'weight')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description')
        }),
        ('Inventory & Availability', {
            'fields': ('stock', 'minimum_order_quantity', 'is_featured', 'is_available')
        }),
        ('Product Media', {
            'fields': ('image', 'image_detail_preview', 'secondary_image', 'secondary_image_detail_preview')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "No Image"
    image_preview.short_description = "Main Image"

    def image_detail_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" max-width="300" style="max-height: 200px; border-radius: 8px;" />')
        return "No Image"
    image_detail_preview.short_description = "Main Image Preview"

    def secondary_image_detail_preview(self, obj):
        if obj.secondary_image:
            return mark_safe(f'<img src="{obj.secondary_image.url}" max-width="300" style="max-height: 200px; border-radius: 8px;" />')
        return "No Secondary Image"
    secondary_image_detail_preview.short_description = "Secondary Image Preview"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'name', 'review')
    readonly_fields = ('product', 'name', 'rating', 'review', 'created_at')


admin.site.register(ProductGallery)
@admin.register(CashewGrade)
class CashewGradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
