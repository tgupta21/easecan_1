from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User
from user.models import PaymentApp, Merchant, Customer, Payer
from transaction.models import Payment, PaymentRequest
from directory.models import Directory
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone', 'email', 'user_type']
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'user_type', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'user_type', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Merchant)
admin.site.register(PaymentApp)
admin.site.register(Customer)
admin.site.register(Payer)
admin.site.register(Payment)
admin.site.register(PaymentRequest)
admin.site.register(Directory)
