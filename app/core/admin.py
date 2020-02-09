from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User
from user.models import Bank, Shop, Website
from transaction.models import Transaction
from directory.models import Directory
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
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
            'fields': ('phone', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Shop)
admin.site.register(Website)
admin.site.register(Bank)
admin.site.register(Transaction)
admin.site.register(Directory)
