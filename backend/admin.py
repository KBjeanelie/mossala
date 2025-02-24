from django.contrib import admin

from backend.models.domain_manager import Domain, Job, Specialty

per_page = 15

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ['name', 'description']
    list_filter = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['name']
    save_on_top = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = per_page


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'description', 'created_at', 'updated_at')
    search_fields = ['name', 'domain__name', 'description']
    list_filter = ['domain', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['name']
    save_on_top = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = per_page


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'specialty', 'description', 'created_at', 'updated_at')
    search_fields = ['title', 'specialty__name', 'description']
    list_filter = ['specialty', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['title']
    save_on_top = True
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = per_page
