# Generated by Django 2.0.1 on 2018-01-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0004_auto_20180110_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='pin_bcm',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]