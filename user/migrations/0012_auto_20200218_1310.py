# Generated by Django 2.2.5 on 2020-02-18 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20200217_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='confirm_token',
            field=models.CharField(max_length=24, unique=True),
        ),
    ]
