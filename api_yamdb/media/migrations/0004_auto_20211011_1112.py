# Generated by Django 2.2.16 on 2021-10-11 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20211009_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genres',
            old_name='genre_name',
            new_name='name',
        ),
    ]