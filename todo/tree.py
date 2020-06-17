from .models import Todo, Label
from django.urls import reverse


class TodoTree(object):
    def __init__(self, root: Label):
        self.children = [TodoSubTree(node) for node in root.todo_set.iterator()]
        self.root = root

    def __repr__(self):
        return '''
            <div class="uk-tile uk-padding-small uk-margin todo-tile-1">
                <div>
                    <a href="{}" class="uk-button uk-button-primary uk-button-small create"> create a todo </a>
                </div>
                {}
            </div>
        '''.format(reverse('create_todo_by_label', args=[self.root.pk]),
                   ''.join([str(todo) for todo in self.children]))


class TodoSubTree(object):
    def __init__(self, todo: Todo):
        self.todo = todo
        self.children = [TodoSubTree(node) for node in todo.todo_set.iterator()]

    def __str__(self):
        return '''
            <div class="uk-tile uk-padding-small uk-margin todo-tile-1">
                <span class="uk-h4"> {} </span>
                <div>
                    <a href="{}" class="uk-button uk-button-primary uk-button-small create"> create a todo </a>
                    <a href="{}" class="uk-button uk-button-primary uk-button-small {}"> {} </a>
                </div>
                {}
            </div>
        '''.format(self.todo.task,
                   reverse('create_todo_by_todo', args=[self.todo.pk]),
                   reverse('todo_toggle_completion', args=[self.todo.pk]),
                   'positive' if not self.todo.is_complete else 'negative',
                   'affirmative 🔥' if not self.todo.is_complete else 'its negative 👍',
                   ''.join([str(todo) for todo in self.children]))

    def __repr__(self):
        return self.__str__()
