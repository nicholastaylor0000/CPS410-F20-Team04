# Generated by Django 2.2.5 on 2020-11-11 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20200303_1426'),
        ('museum', '0009_group_leaders'),
        ('scheduler', '0002_auto_20201111_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='schedule.Event')),
                ('is_claimed', models.BooleanField(default=False, verbose_name='Event is claimed and confirmed')),
                ('copilot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='copilot_event', to='user.UserProfile')),
                ('pilot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pilot_event', to='user.UserProfile')),
                ('simulator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='museum.Simulator')),
            ],
            bases=('schedule.event',),
        ),
        migrations.DeleteModel(
            name='GameEvent',
        ),
    ]
