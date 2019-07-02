from django.contrib import admin
from .models import image, appearance, Category
# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display=['title','photographer','upload_date', 'downloads']
    readonly_fields = ('upload_date',)

admin.site.register(image, ImageAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']

admin.site.register(Category, CategoryAdmin)

class AppearanceAdmin(admin.ModelAdmin):
    list_display=['background_image_link']

admin.site.register(appearance, AppearanceAdmin)
