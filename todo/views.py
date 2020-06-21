from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_list_or_404, get_object_or_404, redirect
from .forms import LabelForm, TodoForm, RewardForm
from .models import Label, Todo, Reward
from .tree import TodoTree


def homepage(request):
    if request.user.is_authenticated:
        return redirect('label_index')
    return render(request, template_name='homepage.html')


@login_required
def label_index(request):
    labels = Label.objects.filter(created_by=request.user)
    context = {'labels': labels}
    return render(request, template_name='label/index.html', context=context)


@login_required
def create_label(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            label = Label(title=form.cleaned_data['title'],
                          description=form.cleaned_data['description'],
                          created_by=request.user)
            label.save()
            return redirect('label_index')
    else:
        form = LabelForm()
    context = {'form': form}
    return render(request, template_name='label/create.html', context=context)


@login_required
def label_detail(request, label_id):
    label = get_object_or_404(Label, pk=label_id)
    if label.created_by.pk is not request.user.pk:
        return render(request, template_name='notauthorised.html')

    todo_tree = TodoTree(label)
    todo_list = Todo.objects.filter(parent_label=label)
    context = {'label': label, 'todo_list': todo_list, 'todo_tree': todo_tree}
    return render(request, template_name='label/detail.html', context=context)


@login_required
def create_todo(request, parent_todo_id=None, parent_label_id=None):
    parent_label = parent_todo = None
    if parent_todo_id:
        parent_todo = get_object_or_404(Todo, pk=parent_todo_id)
        if parent_todo.root_label.created_by.pk is not request.user.pk:
            return render(request, template_name='notauthorised.html')
    if parent_label_id:
        parent_label = get_object_or_404(Label, pk=parent_label_id)
        if parent_label.created_by.pk is not request.user.pk:
            return render(request, template_name='notauthorised.html')

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = Todo(task=form.cleaned_data['task'])
            if parent_todo_id:
                todo.parent_todo = parent_todo
            else:
                todo.parent_label = parent_label
            todo.save()

            return redirect('label_detail', todo.root_label.pk)
    else:
        form = TodoForm()

    context = {
        'parent_todo': parent_todo,
        'parent_label': parent_label,
        'form': form
    }

    return render(request, template_name='todo/create.html', context=context)


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    root_label = todo.root_label
    if root_label.created_by.pk is not request.user.pk:
        return render(request, template_name='notauthorised.html')
    todo.delete()
    return redirect('label_detail', root_label.id)


@login_required
def todo_toggle_completion(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if todo.root_label.created_by.pk is not request.user.pk:
        return render(request, template_name='notauthorised.html')
    todo.is_complete = False if todo.is_complete else True
    todo.save()
    return redirect('label_detail', todo.root_label.pk)


@login_required
def create_reward(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if todo.root_label.created_by.pk is not request.user.pk:
        return render(request, template_name='notauthorised.html')

    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            reward = Reward(description=form.cleaned_data['description'])
            reward.associated_with = todo
            reward.save()
            return redirect('label_detail', todo.root_label.pk)
    else:
        form = RewardForm()
    context = {'form': form, 'todo': todo}
    return render(request, template_name='reward/create.html', context=context)
