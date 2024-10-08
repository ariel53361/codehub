# Generated by Django 5.0.6 on 2024-08-14 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_room_topic_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.svg', null=True, upload_to='avatars'),
        ),
    ]
