# Generated by Django 5.0.6 on 2024-12-17 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_remove_userprofile_password_remove_userprofile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]