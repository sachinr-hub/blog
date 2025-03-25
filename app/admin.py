from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BlogPost, Comment, Category

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('is_staff', 'is_active', 'created_at')
    ordering = ('-created_at',)
    
    # Add custom fields to the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('full_name', 'bio', 'location', 'website', 'profile_picture')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Comment'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    ordering = ('name',)
