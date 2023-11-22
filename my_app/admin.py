from django.contrib import admin
from .models import UserProfileInfo, Product, Order, Movement, DemandSupplyMovement, UserProfileInfoProduct,SearchOrder, SearchMovement
from django.contrib.auth.models import User


admin.site.register(UserProfileInfo)
admin.site.register(Product)
admin.site.register(UserProfileInfoProduct)
admin.site.register(Order)
admin.site.register(Movement)
admin.site.register(DemandSupplyMovement)
admin.site.register(SearchOrder)
admin.site.register(SearchMovement)

