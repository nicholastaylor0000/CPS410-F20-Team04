# Generated by Django 2.2.5 on 2020-01-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20191030_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=48)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
    ]