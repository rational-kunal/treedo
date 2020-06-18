from django.apps import AppConfig


class TodoConfig(AppConfig):
    name = 'todo'
    verbose_name = 'todo'

    def ready(self):
        import todo.signals
