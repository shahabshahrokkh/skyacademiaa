"""Portfolio admin configuration."""

from django.contrib import admin
from .models import Project, ProjectCategory, ProjectGallery


class ProjectGalleryInline(admin.TabularInline):
    model = ProjectGallery
    extra = 3


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active')
    search_fields = ('title', 'client', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectGalleryInline]
