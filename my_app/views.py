from msilib import sequence
import re
from unicodedata import name
from django.shortcuts import render, HttpResponse
from django.core import serializers
from itsdangerous import json

from numpy import product, source
from .forms import UserForm, UserProfileForm, ProductForm, UserProfileProductForm, OrderForm, User, SearchOrderForm, SearchMovementForm
from .models import SearchMovement, UserProfileInfo, Product, UserProfileInfoProduct, Order, Movement, DemandSupplyMovement, SearchOrder
from django.db.models import Sum, Q

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse




def index(request):
    context = {}
    return render(request, 'my_app/index.html', context)

def index_login(request):
    user_obj = UserProfileInfo.objects.filter(user__username=request.user.username)
    membership_type = user_obj[0].membership_type
    context = {'membership_type':membership_type}
    return render(request, 'my_app/index_login.html', context)



def register(request):
    registered = False

    if request.method == 'POST':
        
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()  

            profile = user_profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
    return render(request,'my_app/registration.html',
                 {'user_form':user_form,
                 'user_profile_form':user_profile_form,
                 'registered':registered
                 })
                 

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # print(UserProfileInfo.objects.all())
                user_obj = UserProfileInfo.objects.filter(user__username=username)
                membership_type = user_obj[0].membership_type

                if membership_type == 'regular_customer':
                    return HttpResponseRedirect(reverse('my_app:regular_customer'))
                elif membership_type == 'site_admin':
                    return HttpResponseRedirect(reverse('my_app:site_admin'))
                elif membership_type == 'supplier':
                    return HttpResponseRedirect(reverse('my_app:supplier'))
                elif membership_type == 'drugstore':
                    return HttpResponseRedirect(reverse('my_app:drugstore'))        

                else:
                    return HttpResponse('Please check the code!')    
            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE')
        else:
            return HttpResponse('Invalid login details supplied') 
 

    else:
        return render(request,'my_app/login.html', {}) 


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('my_app:index'))


@login_required
def site_admin(request):
    product_form = ProductForm()
    product_list = Product.objects.order_by('id')
    user_profile_list = UserProfileInfo.objects.order_by('id')
    user_profile_product_form = UserProfileProductForm()
    user_profile_product_list = UserProfileInfoProduct.objects.order_by('id')
    movement_list = Movement.objects.order_by('id')
    demand_supply_movement_list = DemandSupplyMovement.objects.order_by('id')



    context = {'product_form':product_form, 'product_list':product_list,
               'user_profile_list':user_profile_list,
               'user_profile_product_form': user_profile_product_form, 'user_profile_product_list':user_profile_product_list,
               'movement_list':movement_list, 'demand_supply_movement_list':demand_supply_movement_list}
    return render(request, 'my_app/site_admin.html', context)



@login_required
def regular_customer(request):
    user_obj = UserProfileInfo.objects.filter(user__username=request.user.username)
    membership_type = user_obj[0].membership_type
    order_form = OrderForm(username=request.user.username, membership_list=['drugstore'])        
    order_list = Order.objects.filter(destination=request.user.id)
    context = {'order_form':order_form, 'order_list':order_list,'membership_type':membership_type}
    return render(request, 'my_app/regular_customer.html', context)








@login_required
def drugstore(request):  
        order_form = OrderForm(username = request.user.username, membership_list=['supplier', 'drugstore'])
        order_list = Order.objects.filter(destination=request.user.id).order_by('id')
        movement_list = Movement.objects.filter(Q(source=request.user.id) | Q(destination=request.user.id)).order_by('id')
        user_obj = UserProfileInfo.objects.filter(user__username=request.user.username)
        membership_type = user_obj[0].membership_type
        context = {'order_form':order_form, 'order_list':order_list,'movement_list':movement_list,'membership_type':membership_type}                      
        return render(request, 'my_app/drugstore.html', context) 


def search_movement_view(request):
    search_movement_form = SearchMovementForm()
    user_obj = UserProfileInfo.objects.filter(user__username=request.user.username)
    membership_type = user_obj[0].membership_type
    context = {'search_movement_form':search_movement_form,'membership_type':membership_type}                       
    return render(request, 'my_app/search_movement.html', context)


@login_required
def search_movement(request):
    if request.method == 'POST':
        search_movement_form = SearchMovementForm(data=request.POST)
        if search_movement_form.is_valid():
            search_movement = search_movement_form.save(commit=True)
            search_movement.save()
            
            search_movement_obj = search_movement
            sequence = Order.objects.get(sequence=search_movement_obj.sequence)
            search_movement_result = Movement.objects.filter(movement_date__range=[search_movement_obj.start_date,search_movement_obj.end_date],
                                                                 source=search_movement_obj.source,destination=search_movement_obj.destination,
                                                                 product=search_movement_obj.product,order=sequence) 
            # print(search_movement_result)
            ser_search_movement_list = []
            if search_movement_result:
                for instance in search_movement_result:
                    ser_instance = serializers.serialize('json', [instance,])
                    ser_search_movement_list.append(ser_instance)

                demand_supply_movement_obj = DemandSupplyMovement()
                result_trace_back=demand_supply_movement_obj.trace_back(demand_movement_list=search_movement_result,movement_result=[])
                ser_result_trace_back =[serializers.serialize('json', [trace_back,]) for trace_back in result_trace_back]
                                                     
                print(ser_search_movement_list)                         
                print(ser_result_trace_back) 
                                                                                                                                   
            else:
                ser_search_movement_list = []
                ser_result_trace_back = []

            return JsonResponse({'ser_search_movement_list':ser_search_movement_list, 'ser_result_trace_back':ser_result_trace_back}, status=200)
        else:
            return JsonResponse({"error": search_movement_form.errors}, status=400)
    else:
        return JsonResponse({'success':False}, status=400)     



def search_order_view(request):
    search_order_form = SearchOrderForm()
    user_obj = UserProfileInfo.objects.filter(user__username=request.user.username)
    membership_type = user_obj[0].membership_type

    context = {'search_order_form':search_order_form,'membership_type':membership_type}    
    return render(request, 'my_app/search_order.html', context)                                            


@login_required
def search_order(request):
    if request.method == 'POST':
        search_order_form = SearchOrderForm(data=request.POST)
        if search_order_form.is_valid():
            search_order = search_order_form.save(commit=True)
            search_order.save()
   
            search_order_obj = search_order
            print(search_order_obj )
            print(search_order_obj.product)
           
            search_order_result = Order.objects.filter(sequence=search_order_obj.sequence,product=search_order_obj.product,
                                                        source=search_order_obj.source, destination=search_order_obj.destination,
                                                        order_date__range=[search_order_obj.start_date,search_order_obj.end_date])
            if search_order_result:                                      
                print(search_order_result)
                ser_search_order_result = []
                for instance in search_order_result:
                    ser_instance = serializers.serialize('json', [instance,])           
                    ser_search_order_result.append(ser_instance)
                
                print(ser_search_order_result)
            else:
                ser_search_order_result = []

            return JsonResponse({'ser_search_order_result':ser_search_order_result}, status=200)    
        else:
            return JsonResponse({"error": search_order_form.errors}, status=400) 
    else:
        return JsonResponse({'success':False}, status=400)


def add_order_regular_customer(request):
    if request.method == 'POST':
        
        source = UserProfileInfo.objects.get(user=request.POST['source'])
        product = Product.objects.get(id=request.POST['product'])
        current_inventory = Movement.objects.filter(destination=source).filter(product=product).aggregate(Sum('remain_quantity'))['remain_quantity__sum']
        quantity = request.POST.get('quantity')

       
        if int(current_inventory) >= int(quantity):
            order_form = OrderForm(data=request.POST)
            if order_form.is_valid():
                order_instance = order_form.save(commit=True)
                order_instance.save()
                ser_order = serializers.serialize('json',[order_instance,])
        

                quantity = request.POST.get('quantity')
                remain_quantity = quantity
                movement_date = datetime.now()
                product = Product.objects.get(id=request.POST['product'])
                order = Order.objects.get(sequence=request.POST['sequence'])
                source = UserProfileInfo.objects.get(user=request.POST['source'])
                destination = UserProfileInfo.objects.get(user=request.POST['destination'])
                movement_obj = Movement(quantity=quantity, remain_quantity=remain_quantity,
                                        movement_date=movement_date, product=product, order=order,
                                        source=source,destination=destination)   
                movement_obj.save()
                ser_movement = serializers.serialize('json',[movement_obj,])
            
                current_movements = Movement.objects.filter(destination=source).filter(product=product).exclude(remain_quantity=0).order_by('movement_date')
                movement_obj.assignment(order_quantity=quantity, current_movements=current_movements,movement_obj=movement_obj)

                return JsonResponse({'ser_order':ser_order, 'ser_movement':ser_movement}, status=200)
            else:
                return JsonResponse({"error": order_form.errors}, status=400)    
        else:
            return HttpResponse('There is Not enough inventory to create an order')   

    else:
        return JsonResponse({'success':False}, status=400)  

    
def get_form_info(request):
    if request.method == 'GET':
        print('******')
        product = request.GET.get('product')
        print(product)
        source = request.GET.get('source')
        print(source)

        # order_form = OrderForm()
        # source = order_form.cleaned_data['source']
        # product = order_form.cleaned_data['product']
        current_inventory = Movement.objects.filter(destination=source).filter(product=product).aggregate(Sum('remain_quantity'))['remain_quantity__sum']
        print('------')
        print(current_inventory)
        ser_current_inventory  = {'current_inventory':current_inventory}

        # ser_current_inventory = serializers.serialize('json',[current_inventory,])
        
        return JsonResponse({'ser_current_inventory':ser_current_inventory}, status=200)




@login_required
def supplier(request):
    user_profile_product_form = UserProfileProductForm(username=request.user.username)
    user_profile_product_list = UserProfileInfoProduct.objects.filter(user_profile_info__user__username=request.user.username)
    movement_list = Movement.objects.filter(Q(source=request.user.id) | Q(destination=request.user.id)).order_by('id')
    user_obj = UserProfileInfo.objects.filter(user__username=request.user.username)
    membership_type = user_obj[0].membership_type
    context = {'user_profile_product_form':user_profile_product_form, 'user_profile_product_list':user_profile_product_list,
               'movement_list':movement_list,'membership_type':membership_type}
    return render(request, 'my_app/supplier.html', context)


@login_required
def add_user_product_supplier(request):
    if request.method == 'POST':
        user_product_form = UserProfileProductForm(data=request.POST)
        if user_product_form.is_valid():
            user_product = user_product_form.save(commit=True)
            user_product.save()
            ser_user_product = serializers.serialize('json',[user_product,])

            quantity = request.POST.get('inventory')
            remain_quantity = quantity
            movement_date = datetime.now()
            product = Product.objects.get(id=request.POST['product'])
            source = UserProfileInfo.objects.filter(membership_type='site_admin')[0]
            destination = UserProfileInfo.objects.filter(user=request.user)[0]
            movement_obj = Movement(quantity=quantity, remain_quantity=remain_quantity,
                                    movement_date=movement_date, product=product,
                                    source=source,destination=destination)   
            movement_obj.save()
            ser_movement = serializers.serialize('json',[movement_obj,])
            
            return JsonResponse({'ser_user_product':ser_user_product, 'ser_movement':ser_movement}, status=200)
        else:
            return JsonResponse({"error": user_product_form.errors}, status=400)
    else:
        return JsonResponse({'success':False}, status=400) 
        

                  

def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid:
            product = product_form.save(commit=True)
            product.save()
    return HttpResponseRedirect(reverse('my_app:site_admin')) 



def add_user_product_admin(request):
    if request.method == 'POST':
        user_product_form = UserProfileProductForm(data=request.POST)
        if user_product_form.is_valid():
            user_product = user_product_form.save(commit=True)
            user_product.save()
    return HttpResponseRedirect(reverse('my_app:site_admin'))

        
                          

        # filters = {'brand': brand, 'colour': colour, 'year': year}
        # second_hand_cars = SecondHandCars.objects.filter(**filters)


 






   

                                                    
                             
        
                                         





    
          
    




       
















