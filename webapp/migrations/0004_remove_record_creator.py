# Generated by Django 4.2 on 2024-04-25 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_record_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='creator',
        ),
    ]
