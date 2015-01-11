from django.contrib import admin

from .models import Hammer, HammerItem, HammerShare

class HammerAdmin( admin.ModelAdmin ):
    ''' Hammer admin '''
    
    
admin.site.register( Hammer, HammerAdmin )
admin.site.register( HammerItem )

admin.site.register( HammerShare )
