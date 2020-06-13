from django.db import models


class Label(models.Model):
    title = models.CharField(max_length=128)

    def __repr__(self):
        return self.title


class Todo(models.Model):
    task = models.CharField(max_length=256)
    is_complete = models.BooleanField(default=False)
    parent_todo = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    parent_label = models.ForeignKey(to=Label, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def is_root(self):
        return self.parent is None

    @property
    def can_complete(self):
        for task in list(self.todo_set):
            if not task.is_complete:
                return False
        return True

    def __repr__(self):
        return self.task + (' Y' if self.is_complete else ' N')
