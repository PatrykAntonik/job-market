# Generated by Django 5.0.3 on 2025-02-09 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JobApp', '0005_alter_user_managers_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
