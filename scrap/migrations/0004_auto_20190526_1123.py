# Generated by Django 2.2.1 on 2019-05-26 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0003_auto_20190525_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='sector_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industries', to='scrap.Sector'),
        ),
    ]
