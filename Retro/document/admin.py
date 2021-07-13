from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe


# Register your models here.
class CustomAdmin(admin.ModelAdmin):
    liste_filter = ('status',)
    date_hierachy = "date_add"
    list_per_page = 6
    actions =('activate','desactivate') 

    def activate(self,request,queryset):
        queryset.update(status=True)
        self.message_user(request,'la selection a été effectué avec succes')
    activate.short_description = "permet d'activer le champs selectionner"

    def desactivate(self,request,queryset):  
        queryset.update(status=False)
        self.message_user(request,'la selection a été effectué avec succes')
    desactivate.short_description = "permet de desactiver le champs selectionner"

class ImageInline(admin.StackedInline):
    model = models.Images
    extra = 0

class ProjetAdmin(CustomAdmin):
    list_display = ('nom','date_add','date_update','status')
    list_display_links = ['nom']
    ordering = ['nom']
    actions = ('activate','desactivate')
    fieldsets = [
                    ("info image",{"fields":["nom"]}),
                    ("standard",{"fields":["status"]})
                ]
    inlines = [
                ImageInline,
    ]


class ImageAdmin(CustomAdmin):
    list_display = ('date_add','date_update','image_view')
    search_fields = ('date_add',)
    ordering = ['date_add']
    fieldsets = [
                ("info image",{"fields":["image"]}),
                ("foreignkeys info",{"fields":["projet"]}),
                ("foreign keys",{"fields":["status"]})
    ]
    def image_view(self,obj):
        return mark_safe("<img src ='{url}' width='100px',height='50px'>".format(url=obj.image.url))



def _register(model,admin_class):
    admin.site.register(model,admin_class)

_register(models.Projet,ProjetAdmin)
_register(models.Images,ImageAdmin)
