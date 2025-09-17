from django.contrib import admin
from .models import  games, kids, kids_games , cards


# Register your models here.
admin.site.register(games)
admin.site.register(kids)
admin.site.register(kids_games)
admin.site.register(cards)
