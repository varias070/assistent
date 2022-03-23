from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from publications.tasks import start_post_publicator

from articles.models import *


class PublishedPostAdmin(admin.ModelAdmin):
    list_display = ("id", "button", "state")
    fields = ("channel", "post", "prodashka", "proxy")

    def button(self, obj):
        return mark_safe(f'<a class="button" href={obj.id} >Опубликовать</a>')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:id>/', self.admin_site.admin_view(self.published))
        ]

        return my_urls + urls

    def published(self, **kwargs):
        start_post_publicator.delay(self.id)


class PostAdmin(admin.ModelAdmin):
    fields = ("title", "text", "image")


admin.site.site_header = 'Ассистент'
admin.site.register(Channel)
admin.site.register(Proxy)
admin.site.register(Prodashka)
admin.site.register(Post, PostAdmin)
admin.site.register(PublishedPost, PublishedPostAdmin)
admin.site.register(Video)
admin.site.register(PublishedVideo)
