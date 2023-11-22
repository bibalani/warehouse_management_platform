from attr import fields
from django import forms
from django.contrib.auth.models import User
from .models import SearchMovement, UserProfileInfo, Product, UserProfileInfoProduct, Order, DemandSupplyMovement, Movement, SearchOrder, SearchMovement
from functools import partial
from django.forms.widgets import DateInput
from django.db.models import Sum






class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control', 'style':'width:400px'})
            


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('membership_type',) 

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control', 'style':'width:400px'})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'produced_date', 'expired_date', 'company')
        widgets = {
            'produced_date': DateInput(attrs={'type': 'date'}),
            'expired_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:        
            self.fields[field].widget.attrs.update({'class':'form-control'})

    

class UserProfileProductForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfoProduct
        fields = '__all__'
        widgets = {
            'delivery_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, username=None, **kwargs):
        super(UserProfileProductForm, self).__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

        if username:
            self.fields['user_profile_info'].queryset = User.objects.filter(username=username)    





class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'order_date': DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, username=None, membership_list=None, **kwargs):
        super(OrderForm, self).__init__(**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'}) 
        self.fields['sequence'].widget.attrs.update({'class':'form-control','readonly':'readonly'}) 

        if username and membership_list:
            self.fields['destination'].queryset = User.objects.filter(username=username)
            self.fields['source'].queryset = UserProfileInfo.objects.filter(membership_type__in=membership_list).exclude(user__username=username)
            
            
            
            
            if Order.objects.order_by('-id'):   
                print(Order.objects.order_by('-id')[0].sequence)     
                self.fields['sequence'].initial = int(Order.objects.order_by('-id')[0].sequence) + 1 
            else:
                self.fields['sequence'].initial = 1000

            # data = super(OrderForm, self).clean()
            # print(data.get('source'))
            # print(self.fields['product'])
            # source = UserProfileInfo.objects.get(user=self.fields['source'])
            # product = Product.objects.get(name=self.fields['product'])
            # self.fields['quantity'].initial = Movement.objects.filter(destination=self.fields['source'].value()).filter(product=current_product).aggregate(Sum('remain_quantity'))['remain_quantity__sum']
            # print(Movement.objects.filter(destination=current_source).filter(product=current_product).aggregate(Sum('remain_quantity'))['remain_quantity__sum'])
                





class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = '__all__'
        widgets = {
            'movement_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(MovementForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})    



class DemandSupplyMovementForm(forms.ModelForm):
    class Meta:
        model = DemandSupplyMovement
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super(DemandSupplyMovementForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})         




class SearchOrderForm(forms.ModelForm):
    class Meta:
        model = SearchOrder
        fields = ('sequence', 'product', 'source', 'destination', 'start_date', 'end_date')
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})    

        

class SearchMovementForm(forms.ModelForm):
    class Meta:
        model = SearchMovement
        fields = ('product', 'sequence', 'source', 'destination', 'start_date', 'end_date')
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(SearchMovementForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})    






          