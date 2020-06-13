from django import forms


def generic_widget(what, classname='input', placeholder=''):
    return what({'class': classname, 'placeholder': placeholder})


class LabelForm(forms.Form):
    title = forms.CharField(max_length=128,
                            label='title',
                            widget=generic_widget(what=forms.TextInput, placeholder='this will be root of todo tree'))


class TodoForm(forms.Form):
    task = forms.CharField(max_length=256, label='task to do')
