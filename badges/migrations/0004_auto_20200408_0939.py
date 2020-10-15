# Generated by Django 2.2.5 on 2020-04-08 14:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0003_badge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]