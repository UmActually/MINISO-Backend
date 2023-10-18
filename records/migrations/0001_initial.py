# Generated by Django 4.2.6 on 2023-10-17 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('indicators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.FloatField()),
                ('note', models.TextField(null=True)),
                ('health_indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicators.healthindicator')),
            ],
        ),
    ]
