# Generated by Django 2.2.7 on 2019-11-16 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headway', '0004_auto_20191111_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='harvest_id',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
    ]
