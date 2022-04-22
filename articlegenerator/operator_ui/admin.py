from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path

from . import views

from articles.models import *


class PublishedPostAdmin(admin.ModelAdmin):
    list_display = ("post", 'channel', "button", "state")
    fields = ("channel", "post", "prodashka", "proxy")

    def get_urls(self):
        urls = super().get_urls()
        customize_urls = [
            path('publicator/<int:pk>/', views.publish_post, name='publicator')
        ]

        return customize_urls + urls

    @staticmethod
    def button(obj):
        # url = reverse('admin:publicator', kwargs={int: obj.pk})
        return mark_safe(f'<a class="button" href="publicator/{obj.pk}">Опубликовать</a>')


class PostAdmin(admin.ModelAdmin):
    fields = ("title", "text", "image")


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("header", "id")


class PublishArticleAdmin(admin.ModelAdmin):
    list_display = ("article", "channel", "button", "state")
    fields = ("channel", "article", "prodashka", "proxy")

    @staticmethod
    def button(obj):
        return mark_safe(f'<a class="button" href="publicator/{obj.pk}">Опубликовать</a>')

    def get_urls(self):
        urls = super().get_urls()
        customize_urls = [
            path('publicator/<int:pk>/', views.publish_article)
        ]

        return customize_urls + urls


class VideoAdmin(admin.ModelAdmin):
    list_display = ("header", "id")


class PublishVideoAdmin(admin.ModelAdmin):
    list_display = ("video", "channel", "button", "state")
    fields = ("channel", "video", "prodashka", "proxy")

    @staticmethod
    def button(obj):
        return mark_safe(f'<a class="button" href="publicator/{obj.pk}">Опубликовать</a>')

    def get_urls(self):
        urls = super().get_urls()
        customize_urls = [
            path('publicator/<int:pk>/', views.publish_video)
        ]

        return customize_urls + urls


admin.site.site_header = 'Ассистент'
admin.site.register(Article, ArticleAdmin)
admin.site.register(PublishedArticle, PublishArticleAdmin)
admin.site.register(Channel)
admin.site.register(Proxy)
admin.site.register(Prodashka)
admin.site.register(Post, PostAdmin)
admin.site.register(PublishedPost, PublishedPostAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(PublishedVideo, PublishVideoAdmin)
