from django import forms


def generic_widget(what, classname='uk-input', placeholder=''):
    return what({'class': classname, 'placeholder': placeholder})


class LabelForm(forms.Form):
    title = forms.CharField(max_length=128,
                            label='title',
                            widget=generic_widget(what=forms.TextInput, placeholder='this will be root of todo tree'))
    description = forms.CharField(max_length=256,
                                  label='description',
                                  widget=generic_widget(what=forms.Textarea,
                                                        classname='uk-textarea',
                                                        placeholder='some description about label'))


class TodoForm(forms.Form):
    task = forms.CharField(max_length=256,
                           label='task to do',
                           widget=generic_widget(what=forms.TextInput, placeholder='task to do'))
