# Generated by Django 2.1.7 on 2019-03-09 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('importCsv', '0002_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='importCsv.City')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
