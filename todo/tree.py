from .models import Todo, Label
from django.urls import reverse
from common.uikit import UIKit


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
        add_button_link = reverse('create_todo_by_todo', args=[self.todo.pk])
        add_button = UIKit.link_black_hover(href=add_button_link,
                                            text=UIKit.BRANCH_ICON + ' ' + UIKit.ADD_ICON,
                                            css_class_list=['create'])

        control_button = UIKit.link_black_hover(href=reverse('todo_toggle_completion', args=[self.todo.pk]),
                                                text=UIKit.CHECK_ICON if not self.todo.is_complete else UIKit.UNCHECK_ICON,
                                                css_class_list=[
                                                    'positive' if not self.todo.is_complete else 'negative'])

        if not self.todo.can_complete:
            control_button = ''

        delete_button_link = reverse('delete_todo', args=[self.todo.pk])
        delete_button = UIKit.link_black_hover(href=delete_button_link,
                                               text=UIKit.TRASH_ICON,
                                               css_class_list=['delete'])

        create_reward_button_link = reverse('create_reward', args=[self.todo.pk])
        create_reward_button = UIKit.link_black_hover(href=create_reward_button_link,
                                                      text=UIKit.STAR_ICON,
                                                      css_class_list=['create'])

        dropdown = UIKit.drop_down(UIKit.MORE_ICON, [{'link': add_button_link, 'text': 'Add todo in this tree'},
                                                     {'link': delete_button_link, 'text': 'Delete this todo'},
                                                     {'link': create_reward_button_link, 'text': 'create reward'}])

        button_group = UIKit.button_group([add_button, control_button, delete_button, create_reward_button])
        button_group_on_small = UIKit.button_group([control_button, dropdown])

        return '''
            <div class="uk-tile uk-padding-small uk-margin {}">
                <div>
                <span> {} </span>
                <div class="uk-align-right margin-bottom-remove uk-visible@s"> {} </div>
                <div class="uk-align-right margin-bottom-remove uk-hidden@s"> {} </div>
                </div>

                <div>
                    {}
                </div>
                
                {}
            </div>
        '''.format('todo-complete-tile' if self.todo.is_complete else 'todo-tile',
                   self.todo.task,
                   button_group,
                   button_group_on_small,
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

    control_button_group = '<div class="uk-button-group uk-align-right">{}{}</div>'.format(
        claim_button if claim_button_should_show else "", delete_button
    )

    return '<div class="uk-tile uk-padding-small uk-margin-small-top reward-tile">{}{}</div>'.format(
        reward.description, control_button_group
    )
