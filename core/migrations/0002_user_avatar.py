# Generated by Django 5.0.6 on 2024-07-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='default_avatar', upload_to='avatars'),
        ),
    ]
