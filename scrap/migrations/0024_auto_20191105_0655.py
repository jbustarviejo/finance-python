# Generated by Django 2.2.5 on 2019-11-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0023_auto_20190719_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='analisys',
            name='kernel',
            field=models.CharField(blank=True, help_text='kernel type', max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='analisys',
            unique_together={('company', 'kernel', 'svm', 'number_of_days_sample')},
        ),
        migrations.RemoveField(
            model_name='analisys',
            name='degree',
        ),
    ]