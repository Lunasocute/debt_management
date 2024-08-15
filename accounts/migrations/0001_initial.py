# Generated by Django 4.2 on 2024-08-14 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('ssn', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_reference_no', models.CharField(max_length=255)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField(choices=[(0, 'INACTIVE'), (1, 'PAID_IN_FULL'), (2, 'IN_COLLECTION')], default=0)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.agency')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.client')),
                ('consumers', models.ManyToManyField(to='accounts.consumer')),
            ],
        ),
    ]
