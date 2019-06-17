# Generated by Django 2.2.1 on 2019-06-16 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0018_auto_20190611_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='svm_updated_at',
            field=models.DateTimeField(blank=True, help_text='Updated SVM time', null=True),
        ),
        migrations.CreateModel(
            name='Analisys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kernel', models.CharField(blank=True, help_text='Kernel of the SVM', max_length=100, null=True)),
                ('svm', models.CharField(blank=True, help_text='SVM type', max_length=100, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
                ('number_of_days_sample', models.IntegerField(blank=True, max_length=100, null=True)),
                ('number_of_train_vectors', models.IntegerField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='scrap.Company')),
            ],
            options={
                'unique_together': {('company', 'kernel', 'svm')},
            },
        ),
    ]
