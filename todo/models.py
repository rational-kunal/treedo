from django.db import models
from accounts.models import User


class Label(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return self.title


class Todo(models.Model):
    task = models.CharField(max_length=256)
    is_complete = models.BooleanField(default=False)
    parent_todo = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    parent_label = models.ForeignKey(to=Label, on_delete=models.CASCADE, blank=True, null=True)
    _root_label = models.ForeignKey(to=Label, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='root_label')

    @property
    def is_root(self):
        return self.parent_todo is None

    @property
    def can_complete(self):
        for task in self.todo_set.iterator():
            if not task.is_complete:
                return False
        return True

    @property
    def root_label(self):
        if self._root_label is not None:
            return self._root_label
        node = self.parent_todo
        label = self.parent_label
        while node is not None:
            label = node.parent_label
            node = node.parent_todo
        return label

    def __repr__(self):
        return self.task + (' Y' if self.is_complete else ' N')


class Reward(models.Model):
    description = models.CharField(max_length=128)
    associated_with = models.ForeignKey(to=Todo, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.__str__()
