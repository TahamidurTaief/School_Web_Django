# notice/admin.py

from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Notice, NoticeType

# --- IMPORTS FOR UNFOLD AND IMPORT/EXPORT ---
# from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin

# --- COMBINED ADMIN CLASS FOR UNFOLD + IMPORT/EXPORT ---
class CustomNoticeModelAdmin(ImportExportModelAdmin, ModelAdmin):
    pass

@admin.register(NoticeType)
class NoticeTypeAdmin(CustomNoticeModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',) # Required for autocomplete_fields in NoticeAdmin
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Notice)
class NoticeAdmin(CustomNoticeModelAdmin):
    list_display = ('title', 'notice_type', 'class_name', 'department', 'is_active', 'created_at')
    list_filter = ('notice_type', 'class_name', 'department', 'is_active')
    search_fields = ('title', 'short_description')
    date_hierarchy = 'created_at'
    
    # Using autocomplete_fields for a much better UX than raw_id_fields
    autocomplete_fields = ('notice_type', 'class_name', 'department')
    
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Notice Information', {
            'fields': ('title', 'short_description', 'file')
        }),
        ('Categorization & Targeting', {
            'description': "Select a category and, if applicable, a specific class or department this notice is for.",
            'fields': ('notice_type', 'class_name', 'department')
        }),
        ('Status', {
            'fields': ('is_active', ('created_at', 'updated_at'))
        }),
    )