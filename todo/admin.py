from django.contrib import admin
from .models import Todo, Label, Reward

admin.site.register(Label)
admin.site.register(Todo)
admin.site.register(Reward)
