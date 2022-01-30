from django.contrib import admin

from .models import Sezione , Discussione , Post

# Register your models here.

class DiscussioneModelAdmin(admin.ModelAdmin):
    list_display = ['titolo','autore','data']
    list_filter = ['titolo','autore']

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['autore','data']
    list_filter = ['autore','data']

admin.site.register(Sezione)
admin.site.register(Discussione , DiscussioneModelAdmin)
admin.site.register(Post,PostModelAdmin)