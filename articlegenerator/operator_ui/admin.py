from django.contrib import admin
from django.utils.safestring import mark_safe

from articles.models import *


class PublishedPostAdmin(admin.ModelAdmin):
    list_display = ("post", "button",)

    def button(self, obj):
        return mark_safe(f'<a class="button" href='' >Опубликовать</a>')


admin.site.site_header = 'Ассистент'
admin.site.register(Chanel)
# admin.site.register(Image)
# admin.site.register(Article)
# admin.site.register(PostImage)
admin.site.register(Prodashka)
admin.site.register(Post)
admin.site.register(PublishedPost, PublishedPostAdmin)
# admin.site.register(Published)

