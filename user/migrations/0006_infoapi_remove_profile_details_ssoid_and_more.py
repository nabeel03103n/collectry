# Generated by Django 5.0.6 on 2024-12-02 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_profile_details_merchantid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoAPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ssoid', models.CharField(max_length=30)),
                ('merchantid', models.CharField(max_length=30)),
                ('emali', models.EmailField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile_details',
            name='SSOID',
        ),
        migrations.RemoveField(
            model_name='profile_details',
            name='merchantId',
        ),
        migrations.RemoveField(
            model_name='profile_details',
            name='user',
        ),
    ]
