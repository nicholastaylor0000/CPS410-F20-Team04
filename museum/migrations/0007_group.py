# Generated by Django 2.2.5 on 2020-02-04 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20200130_1119'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museum', '0006_auto_20191125_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('museum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum.Museum')),
                ('profiles', models.ManyToManyField(to='user.UserProfile')),
            ],
        ),
    ]
