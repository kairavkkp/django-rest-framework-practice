from django.contrib import admin
from api.models import PaymentMethod, KSUser, Game, GameCategory, \
    Price, Order, Wishlist, Library

# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(KSUser)
admin.site.register(Game)
admin.site.register(GameCategory)
admin.site.register(Price)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Library)
