from django.contrib import admin
from .models import *
admin.site.register(Category)
#admin.site.register(Category,CategoryAdmin)
admin.site.register(Place)
admin.site.register(Portfolio)
