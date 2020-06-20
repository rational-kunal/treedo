from .models import Todo, Label
from django.urls import reverse


class TodoTree(object):
    def __init__(self, root: Label):
        self.children = [TodoSubTree(node) for node in root.todo_set.iterator()]
        self.root = root

    def __repr__(self):
        return '''
            <div class="uk-tile uk-padding-remove uk-margin">
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
        control_button_link = reverse('todo_toggle_completion', args=[self.todo.pk])
        control_button_class = 'positive' if not self.todo.is_complete else 'negative'
        control_button_text = 'affirmative 🔥' if not self.todo.is_complete else 'its negative 👎'

        control_button = '<a href="{}" class="uk-button uk-button-primary uk-button-small {}"> {} </a>'.format(
            control_button_link, control_button_class, control_button_text
        ) if self.todo.can_complete else ""

        delete_button_link = reverse('delete_todo', args=[self.todo.pk])
        delete_button = '<a href="{}" class="uk-button uk-button-secondary delete uk-button-small"> delete </a>'.format(
            delete_button_link
        )

        completed_icon = '(<span uk-icon="check"></span>)' if self.todo.is_complete else ''

        return '''
            <div class="uk-tile uk-padding-small uk-margin todo-tile">
                <span class="uk-h4"> {} {} </span>
                <div>
                <div class="uk-button-group">
                    <a href="{}" class="uk-button uk-button-primary uk-button-small create"> create a todo </a>
                    {}
                    {}
                </div>
                </div>
                {}
            </div>
        '''.format(completed_icon,
                   self.todo.task,
                   reverse('create_todo_by_todo', args=[self.todo.pk]),
                   control_button,
                   delete_button,
                   ''.join([str(todo) for todo in self.children]))

    def __repr__(self):
        return self.__str__
