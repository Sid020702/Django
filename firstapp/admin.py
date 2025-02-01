from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, CustomUser

from .models import Cart, Product, ProductInCart, Order, Deal
from .forms import  CustomUserCreationForm, CustomUserChangeForm


class CartInline(admin.TabularInline):
    model = Cart

class DealInline(admin.TabularInline):
    model=Deal.user.through

class ProductInCartInline(admin.TabularInline):
    model=ProductInCart


class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    list_display=('email','is_staff', 'is_active')
    list_filter=('email','is_staff', 'is_active')

    fieldsets=(
        (None, {'fields':('email','password')})
        ('Permissions',{'fields':('is_staff','is_active')})
    )

    add_fieldsets=(
        (None, {
        'classes':('wide',),
        'fields':('email', 'password1','password2','is_staff','is_active')
        })
    )

    search_fields=('email',)
    ordering=('email',)


class UserAdmin(UserAdmin):
    model = User
    list_display=('username','get_cart','is_staff','is_active')
    list_filter=('username','is_staff','is_active','is_superuser')
    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Permissions',{'fields':('is_staff',('is_active','is_superuser'))}),
        ('Important Dates',{'fields':('last_login','date_joined')}),
        ('Advanced options',{
            'classes': ('collapse'),
            'fields':('groups','user_permissions')
        })
    )

    add_fieldsets=(
        (None, {
            'classes':('wide'),
            'fields':('username','password1','password2','is_staff','is_active','is_superuser','groups')
        })
    )



    def get_cart(self,obj):
        return obj.cart

    inlines=[CartInline, DealInline]# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    mode = User
    list_display=('staff','user','created_on')
    list_filter=('user','created_on')

    fieldsets=(
        (None,{'fields':('user','created_on')}),
        ('User',{'fields':('user_email','staff')})
    )

    readonly_fields = ['user_email', 'staff']

    inlines=[
        ProductInCartInline
    ]


    def staff(self, obj):
        return obj.user.is_staff
    
    def user_email(self, obj):
        """Display the email of the related user."""
        return obj.user.email if obj.user else "N/A"
    

    staff.admin_order_field = 'user__is_staff'
    staff.short_description='Staff User'

    list_filter=['user__is_staff', 'created_on']
    search_fields=['user__username']

class DealAdmin(admin.ModelAdmin):
    inlines=[
        DealInline
    ]

    exclude=('user',)

admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)
admin.site.register(Deal, DealAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)