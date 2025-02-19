from django.contrib import admin

from authentication.models import User, UserStatus

# Register your models here.
@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['id','status']
    search_fields = ['id','status']
    list_filter = ['id','status']
    ordering = ['id','status']
    fieldsets = (
        (None, {
            'fields': ('status',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('status',)
        }),
    )
    show_full_result_count = False
    show_change_link = True
    show_full_result_count = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','tel','email','email_verified','date_joined','last_login','is_staff','is_active','is_superuser']
    search_fields = ['id','tel','email','is_staff','is_active','is_superuser']
    list_filter = ['id','username','tel','email','email_verified','date_joined', 'is_staff','is_active','is_superuser']
    ordering = ['id','tel','email','is_staff','is_active','is_superuser']
    
    fieldsets = (
        (None, {
            'fields': ('username','tel','email','email_verified','is_staff','is_active','is_superuser',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username','tel','email','email_verified','is_staff','is_active','is_superuser',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    readonly_fields = ['date_joined','last_login']