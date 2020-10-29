# Generated by Django 2.0.1 on 2018-02-18 23:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('motors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('descr', models.CharField(max_length=255)),
                ('logic', models.CharField(max_length=255)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='toggle',
            name='rule',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='motors.Rule'),
            preserve_default=False,
        ),
    ]