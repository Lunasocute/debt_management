# Generated by Django 4.2 on 2024-08-15 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_agency', models.BooleanField()),
                ('data_joined', models.DateField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
