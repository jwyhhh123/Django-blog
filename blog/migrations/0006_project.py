# Generated by Django 2.2.12 on 2020-06-23 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default='')),
                ('end_date', models.DateField(default='')),
                ('place', models.CharField(max_length=80)),
                ('text', models.TextField(default='')),
            ],
        ),
    ]
