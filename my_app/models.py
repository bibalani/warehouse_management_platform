
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import json
from django.core.validators import MaxLengthValidator, MinLengthValidator



class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    membership_choices = (('site_admin', 'SITE_ADMIN'),
                            ('supplier', 'SUPPLIER'),
                            ('drugstore','DRUGSTORE'),
                            ('regular_customer', 'REGULAR_CUSTOMER'))
    membership_type = models.CharField(max_length=50, choices=membership_choices, blank=False)
    
    def __str__(self):
        return self.user.username



class Product(models.Model):
    name = models.CharField(max_length=20)
    produced_date = models.DateField(blank=True)
    expired_date = models.DateField(blank=True)
    company = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

   




class UserProfileInfoProduct(models.Model):
    
    user_profile_info = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inventory = models.IntegerField()
    delivery_date = models.DateField()

    def __str__(self):
        return f'{self.user_profile_info.user.username}-{self.product.name}'





class Order(models.Model):
    sequence = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateField()
    source = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='order_source')
    destination =  models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='order_destination')
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.sequence)

    


   
 


class Movement(models.Model):
    quantity = models.IntegerField()
    remain_quantity = models.IntegerField()
    movement_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True) 
    source = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='movement_source')
    destination = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='movement_destination')

    def __str__(self):
        return f'{self.source.user.username}-{self.destination.user.username}-{self.quantity}-{self.product}-{self.movement_date}'

    def assignment(self, order_quantity,current_movements,movement_obj):
        for movement in current_movements:
            if int(movement.quantity) >= int(order_quantity):
                movement.remain_quantity = int(movement.quantity) - int(order_quantity)
                demand_supply_movement_obj = DemandSupplyMovement(demand_movement=movement_obj,
                                                                  supply_movement=movement, quant=order_quantity) 
                movement.save()                                                    
                demand_supply_movement_obj.save()
                break
            else:
                demand_supply_movement_obj = DemandSupplyMovement(demand_movement=movement_obj,
                                                                  supply_movement=movement, quant=movement.remain_quantity)
                order_quantity = int(order_quantity) - int(movement.remain_quantity)
                movement.remain_quantity = 0
                movement.save()                                                    
                demand_supply_movement_obj.save()
                
                




class DemandSupplyMovement(models.Model):
    demand_movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name='demand_movement')
    supply_movement = models.ForeignKey(Movement, on_delete=models.CASCADE, related_name='supply_movement')
    quant  = models.IntegerField()

    def __str__(self):
        return f'{self.demand_movement}-{self.supply_movement}-{self.quant}'


    def trace_back(self, demand_movement_list, movement_result):
        if demand_movement_list:
            for movement in demand_movement_list:
                if movement.source.user.id == '1':
                    continue
                else:
                    demand_supply_movements = DemandSupplyMovement.objects.filter(demand_movement=movement)
                    new_demand_movement_list = [item.supply_movement for item in demand_supply_movements]
                    movement_result.extend(new_demand_movement_list)
                    
                    self.trace_back(new_demand_movement_list, movement_result)
        return movement_result
            
            
            




class SearchOrder(models.Model):
    sequence = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    source = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='search_order_source')
    destination =  models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='search_order_destination')


class SearchMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sequence = models.IntegerField(null=True)
    source = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='search_movement_source')
    destination =  models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, related_name='search_movement_destination')
    start_date = models.DateField()
    end_date = models.DateField()