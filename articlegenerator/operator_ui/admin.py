from django.contrib import admin
from django.utils.safestring import mark_safe

from articles.models import *


class PublishedPostAdmin(admin.ModelAdmin):
    list_display = ("id", "button", "state")
    fields = ("channel", "post", "prodashka", "proxy")

    def button(self, obj):
        return mark_safe(f'<a class="button" href={obj.id} >Опубликовать</a>')


class PostAdmin(admin.ModelAdmin):
    fields = ("text", "image")


admin.site.site_header = 'Ассистент'
admin.site.register(Channel)
# admin.site.register(Image)
# admin.site.register(Article)
# admin.site.register(PostImage)
admin.site.register(Proxy)
admin.site.register(Prodashka)
admin.site.register(Post, PostAdmin)
admin.site.register(PublishedPost, PublishedPostAdmin)
# admin.site.register(Published)

