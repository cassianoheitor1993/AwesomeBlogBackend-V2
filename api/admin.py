from django.contrib import admin
from .models import Article, Image, Comment, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.html import format_html

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ArticleAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    list_filter = ('author', 'category', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [ImageInline]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'body')
    list_filter = ('author', 'category', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [ImageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('article', 'image_thumbnail', 'image')
    search_fields = ('article__title',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 65px; height:65px;" />'.format(obj.image.url))
        return "-"
    image_thumbnail.short_description = 'Thumbnail'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'created_at')
    search_fields = ('article__title', 'author__username', 'body')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)