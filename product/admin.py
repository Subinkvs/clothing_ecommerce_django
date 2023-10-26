from django.contrib import admin
from product.models import MenClothing,BannerImage,Category

# Register your models here.
class MenClothingAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand', 'size', 'color', 'price')
    list_filter = ('category', 'size', 'color')
    search_fields = ('brand', 'description')
    


admin.site.register(MenClothing, MenClothingAdmin)
admin.site.register(BannerImage)
admin.site.register(Category)
