# Generated by Django 3.2.6 on 2021-09-15 04:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('icon', models.CharField(max_length=30)),
                ('level', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14)])),
                ('order', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('active', models.BooleanField(default=True)),
                ('last_child', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='menu.menu')),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
                'ordering': ('code',),
            },
        ),
    ]