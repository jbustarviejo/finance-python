# Generated by Django 2.2.1 on 2019-06-10 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0016_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='link',
        ),
    ]
