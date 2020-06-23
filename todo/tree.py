from .models import Todo, Label
from django.urls import reverse


class UIKit(object):
    ADD_ICON = '<span uk-icon="icon: plus"></span>'
    CHECK_ICON = '<span uk-icon="icon: check"></span>'
    UNCHECK_ICON = '<span uk-icon="icon: close"></span>'
    TRASH_ICON = '<span uk-icon="icon: trash"></span>'
    STAR_ICON = '<span uk-icon="icon: star"></span>'
    BRANCH_ICON = '<span uk-icon="icon: git-branch"></span>'

    @staticmethod
    def button_group(btn_list):
        return '<div class="uk-button-group"> {} </div>'.format(
            ' '.join(btn_list)
        )

    @staticmethod
    def link_black_hover(href, text, css_class_list):
        return '<a href="{}" class="uk-button uk-button-secondary uk-button-small create {}"> {} </a>'.format(
            href, ' '.join(css_class_list), text
        )


class TodoTree(object):
    def __init__(self, root: Label):
        self.children = [TodoSubTree(node) for node in root.todo_set.iterator()]
        self.root = root

    def __repr__(self):
        return '''
            <div class="uk-tile uk-padding-remove uk-margin">
                <div>
                    <a href="{}" class="uk-button uk-button-secondary uk-button-small create">
                        <span class="uk-margin-small-right"> create a todo </span>
                        {}
                    </a>
                </div>
                {}
            </div>
        '''.format(reverse('create_todo_by_label', args=[self.root.pk]),
                   UIKit.ADD_ICON,
                   ''.join([str(todo) for todo in self.children]))


class TodoSubTree(object):
    def __init__(self, todo: Todo):
        self.todo = todo
        self.children = [TodoSubTree(node) for node in todo.todo_set.iterator()]

    def __str__(self):
        add_button = UIKit.link_black_hover(href=reverse('create_todo_by_todo', args=[self.todo.pk]),
                                            text=UIKit.BRANCH_ICON + ' ' + UIKit.ADD_ICON,
                                            css_class_list=['create'])

        control_button = UIKit.link_black_hover(href=reverse('todo_toggle_completion', args=[self.todo.pk]),
                                                text=UIKit.CHECK_ICON if not self.todo.is_complete else UIKit.UNCHECK_ICON,
                                                css_class_list=[
                                                    'positive' if not self.todo.is_complete else 'negative'])

        if not self.todo.can_complete:
            control_button = ''

        delete_button = UIKit.link_black_hover(href=reverse('delete_todo', args=[self.todo.pk]),
                                               text=UIKit.TRASH_ICON,
                                               css_class_list=['delete'])

        completed_icon = '(<span uk-icon="check"></span>)' if self.todo.is_complete else ''

        create_reward_button = UIKit.link_black_hover(href=reverse('create_reward', args=[self.todo.pk]),
                                                      text=UIKit.STAR_ICON,
                                                      css_class_list=['create'])

        button_group = UIKit.button_group([add_button, control_button, delete_button, create_reward_button])

        return '''
            <div class="uk-tile uk-padding-small uk-margin {}">
                <div>
                <span> {} {} </span>
                <div class="uk-align-right margin-bottom-remove"> {} </div>
                </div>

                <div>
                    {}
                </div>
                
                {}
            </div>
        '''.format('todo-complete-tile' if self.todo.is_complete else 'todo-tile',
                   completed_icon,
                   self.todo.task,
                   button_group,
                   ''.join([reward_tile(reward) for reward in self.todo.reward_set.iterator()]),
                   ''.join([str(todo) for todo in self.children]))

    def __repr__(self):
        return self.__str__


def reward_tile(reward):
    delete_button = '<a href="{}" class="uk-button uk-button-secondary delete uk-button-small" uk-icon="icon: trash"></a>'.format(
        reverse('delete_reward', args=[reward.pk])
    )

    claim_button_link = reverse('reward_toggle_claim', args=[reward.pk])
    claim_button_class = 'positive' if not reward.is_claimed else 'negative'
    claim_button_icon = 'close' if reward.is_claimed else 'check'
    claim_button = '<a href="{}" class="uk-button uk-button-secondary delete uk-button-small {}" uk-icon="icon: {}"> </a>'.format(
        claim_button_link, claim_button_class, claim_button_icon
    )

    claim_button_should_show = reward.can_claim or reward.is_claimed

    control_button_group = '<div class="uk-button-group uk-align-right">{} {}</div>'.format(
        claim_button if claim_button_should_show else "", delete_button
    )

    return '<div class="uk-tile uk-padding-small uk-margin-small-top reward-tile">{}{}</div>'.format(
        reward.description, control_button_group
    )
