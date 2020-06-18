from django.urls import path
from todo import views

urlpatterns = [
    path('label/', views.label_index, name='label_index'),
    path('label/<int:label_id>', views.label_detail, name='label_detail'),
    path('label/create', views.create_label, name='create_label'),

    path('todo/createbylabel/<int:parent_label_id>', views.create_todo, name='create_todo_by_label'),
    path('todo/createbytodo/<int:parent_todo_id>', views.create_todo, name='create_todo_by_todo'),
    path('todo/toggle/<int:todo_id>', views.todo_toggle_completion, name='todo_toggle_completion'),

    path('', views.homepage, name='homepage')
]
