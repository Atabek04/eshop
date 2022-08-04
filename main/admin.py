from django.contrib import admin
from main.models import *


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)


# ----------------------------------------------
class SizeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Size, SizeAdmin)


# ----------------------------------------------
class ColorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Color, ColorAdmin)


# ----------------------------------------------
class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)


# ----------------------------------------------
class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductImage, ProductImageAdmin)


# ----------------------------------------------
class CommentItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(CommentItem, CommentItemAdmin)


# ----------------------------------------------
class CartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cart, CartAdmin)



# ----------------------------------------------
class CartItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(CartItem, CartItemAdmin)
