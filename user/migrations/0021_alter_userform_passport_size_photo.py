# Generated by Django 5.0.6 on 2024-12-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_alter_userform_passport_size_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userform',
            name='passport_size_photo',
            field=models.ImageField(blank=True, null=True, upload_to='UserForm/'),
        ),
    ]
