from django.contrib import admin
from . models import Record
from django.contrib.auth.models import Group
# Register your models here.
admin.site.site_header = "CRM Aden"
admin.site.site_title = "CRM Aden"


class RecordAdmin(admin.ModelAdmin):
   list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country', 'creation_date')
   search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country')
   
   
   


admin.site.register(Record,RecordAdmin)
admin.site.unregister(Group)







    
    







