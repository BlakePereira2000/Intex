from django.contrib import admin

from .models import Daily_Journal, Food_in_Day, Food, User, Comorbidity

# Register your models here.
admin.site.register(Food_in_Day)
admin.site.register(Daily_Journal)
admin.site.register(Food)
admin.site.register(User)
admin.site.register(Comorbidity)