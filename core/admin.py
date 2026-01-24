from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# @admin.register(User)  # Pastikan model User didaftarkan dengan dekorator
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'email', 'id_role', 'mobile_phone', 'is_staff', 'is_active')  # Tampilan daftar user
#     list_filter = ('id_role', 'is_staff', 'is_active')  # Filter berdasarkan role
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal Info', {'fields': ('email', 'mobile_phone')}),
#         ('Role & Status', {'fields': ('id_role', 'status')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'mobile_phone', 'id_role', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('username', 'email')
#     ordering = ('username',)
#     filter_horizontal = ('groups', 'user_permissions')

admin.site.register(Role)
admin.site.register(AdminRole)
admin.site.register(User)
admin.site.register(TransactionRule)
admin.site.register(UserTransactionRule)
admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Supplier)
admin.site.register(Flight)
admin.site.register(Hotel)
admin.site.register(Profit)
admin.site.register(SupplierProfit)
