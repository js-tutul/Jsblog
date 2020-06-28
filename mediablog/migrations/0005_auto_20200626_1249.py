# Generated by Django 2.2.7 on 2020-06-26 19:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mediablog', '0004_allreact'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('user', 'post')},
        ),
        migrations.DeleteModel(
            name='Allreact',
        ),
    ]
