# Generated by Django 5.0.6 on 2024-12-04 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_userform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userform',
            old_name='PDF_file',
            new_name='file',
        ),
    ]
