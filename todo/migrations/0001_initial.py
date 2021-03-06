# Generated by Django 3.0.7 on 2020-06-12 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=256)),
                ('is_complete', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='todo.Todo')),
                ('parent_label', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='todo.Label')),
            ],
        ),
    ]
