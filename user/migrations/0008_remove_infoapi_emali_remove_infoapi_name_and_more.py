# Generated by Django 5.0.6 on 2024-12-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_delete_profile_delete_profile_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infoapi',
            name='emali',
        ),
        migrations.RemoveField(
            model_name='infoapi',
            name='name',
        ),
        migrations.AddField(
            model_name='infoapi',
            name='username',
            field=models.CharField(default='username', max_length=100),
            preserve_default=False,
        ),
    ]
