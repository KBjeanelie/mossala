from django.contrib import admin

from authentication.models import  District, Quater, User, UserStatus

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
    list_display = ['id','username','tel','email','email_verified','date_joined','last_login','is_active',]
    search_fields = ['id','tel','email','is_active',]
    list_filter = ['id','username','tel','email','email_verified','date_joined', 'is_active',]
    ordering = ['id','tel','email',]
    
    fieldsets = (
        (None, {
            'fields': ('username','tel','email', 'user_quater',)
        }),
        ('Status', { 'fields': ('status','email_verified', 'is_staff','is_active','is_superuser', 'is_verified')}),
        ('Information Général', {
            'fields': ('photo', 'lastname', 'firstname','nickname', 'gender', 'nationality', 'birthplace', 'date_of_birth',)}),
        ('Réseaux sociaux', {
            'fields': ('skype', 'gmail', 'discord', 'facebook', 'linkedin','instagram', 'twitter', 'whatsapp')}),
        ('Création et modification', {'fields': ('date_joined', 'updated_at')}),
        ('Information Utilisateur', 
            {'fields': ('last_login', 'last_ip', 'last_location', 'imei')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username','tel', 'email', 'password1', 'password2','email_verified','is_staff','is_active','is_superuser' )}),
        
        ('Status', {
            'fields': ('status',)
        }),
    )
    readonly_fields = ['date_joined', 'last_login', 'last_ip', 'last_location', 'imei', 'updated_at']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    search_fields = ['id','name']
    list_filter = ['id','name']
    ordering = ['id','name']
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )
    
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Quater)
class QuaterAdmin(admin.ModelAdmin):
    list_display = ['id','name','district']
    search_fields = ['id','name','district']
    list_filter = ['id','name','district']
    ordering = ['id','name']
    fieldsets = (
        (None, {
            'fields': ('name', 'district')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('name', 'district')
        }),
    )
    readonly_fields = ['id', 'created_at', 'updated_at']

