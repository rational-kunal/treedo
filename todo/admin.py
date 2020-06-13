from django.contrib import admin
from .models import Todo, Label

admin.site.register(Label)
admin.site.register(Todo)
